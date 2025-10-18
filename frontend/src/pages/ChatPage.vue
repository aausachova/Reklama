    <template>
        <section class="h-[calc(100vh-80px)] px-4">
            <div class="h-full flex flex-col">
                <Button variant="outline" class="sm:hidden mb-2" @click="showChatList = true">
                    <Users class="mr-2 size-4" />
                    Список чатов
                </Button>

                <div class="h-full flex-1 sm:grid sm:grid-cols-[350px_1fr] gap-4">
                    <div class="bg-card border rounded-xl flex flex-col" :class="{
                        'fixed inset-0 z-50': !isDesktop,
                        'hidden': !isDesktop && !showChatList,
                        'sm:static sm:block': true
                    }">
                        <div class="flex items-center justify-between border-b p-4">
                            <h2 class="text-lg font-semibold">Сообщения</h2>
                            <Button v-if="!isDesktop" variant="ghost" size="icon" @click="showChatList = false">
                                <X class="size-4" />
                            </Button>
                        </div>
                        <div class="border-b p-4 flex flex-col gap-3">
                            <Input v-model="searchQuery" placeholder="Поиск чата..." class="w-full" />
                        </div>
                        <ScrollArea class="flex-1">
                            <div class="p-3 space-y-2">
                                <template v-if="filteredChats.length">
                                    <button v-for="chat in filteredChats" :key="chat.id"
                                        class="w-full flex items-center gap-3 p-3 rounded-lg hover:bg-muted transition-colors"
                                        :class="{ 'bg-accent': selectedChat?.id === chat.id }" @click="selectChat(chat)">
                                        <Avatar class="size-10 shrink-0">
                                            <AvatarFallback class="bg-primary text-primary-foreground font-semibold">
                                                {{ chat.user.initials }}
                                            </AvatarFallback>
                                        </Avatar>
                                        <div class="flex-1 min-w-0 text-left">
                                            <div class="flex items-center justify-between gap-2">
                                                <p class="font-medium text-sm truncate">{{ chat.user.name }}</p>
                                                <span v-if="chat.lastMessage"
                                                    class="text-xs text-muted-foreground whitespace-nowrap">
                                                    {{ chat.lastMessage.time }}
                                                </span>
                                            </div>
                                            <div class="flex items-center justify-between gap-2">
                                                <p class="text-xs text-muted-foreground truncate">{{ chat.user.role }}</p>
                                                <div v-if="chat.unread" class="size-2 rounded-full bg-primary shrink-0">
                                                </div>
                                            </div>
                                        </div>
                                    </button>
                                </template>
                                <div v-else class="text-center py-8 text-muted-foreground">
                                    Чат не найден
                                </div>
                            </div>
                        </ScrollArea>
                    </div>

                    <div class="bg-card border rounded-xl flex flex-col relative overflow-hidden h-full"
                        :class="{ 'hidden sm:flex': !isDesktop && showChatList }">
                        <div v-if="selectedChat" class="h-full flex flex-col">
                            <div class="flex-none border-b p-4 flex items-center justify-between">
                                <div class="flex items-center gap-3">
                                    <Avatar class="size-10">
                                        <AvatarFallback class="bg-primary text-primary-foreground font-semibold">
                                            {{ selectedChat.user.initials }}
                                        </AvatarFallback>
                                    </Avatar>
                                    <div>
                                        <h3 class="font-medium">{{ selectedChat.user.name }}</h3>
                                        <p class="text-sm text-muted-foreground">{{ selectedChat.user.role }}</p>
                                    </div>
                                </div>
                                <Button variant="ghost" size="icon" class="rounded-full">
                                    <MoreVertical class="size-4" />
                                </Button>
                            </div>

                            <Button variant="secondary" v-if="showScrollDownButton"
                                class="rounded-full p-0 size-10 absolute bottom-20 right-6 z-10" @click="scrollToBottom">
                                <ChevronDown class="size-4" />
                            </Button>

                            <div v-if="!selectedChat.messages.length"
                                class="flex-1 flex items-center justify-center text-muted-foreground">
                                Начните общение прямо сейчас!
                            </div>
                            <div v-else ref="containerRef" @scroll="handleScroll"
                                class="chat-messages flex-1 overflow-y-auto p-4 space-y-4">
                                <div v-for="message in selectedChat.messages" :key="message.id"
                                    :class="['message', message.isOwn ? 'message-self' : 'message-other']">
                                    <div class="flex items-end gap-2" :class="message.isOwn ? 'flex-row-reverse' : ''">
                                        <Avatar v-if="!message.isOwn" class="size-8 mb-1">
                                            <AvatarFallback
                                                class="bg-primary text-primary-foreground text-xs font-semibold">
                                                {{ selectedChat.user.initials }}
                                            </AvatarFallback>
                                        </Avatar>
                                        <div class="space-y-1 max-w-[80%] w-fit">
                                            <div class="break-words  px-4 py-2.5 whitespace-pre-wrap" :class="message.isOwn ? [
                                                'bg-primary text-primary-foreground',
                                                'rounded-t-2xl rounded-bl-2xl'
                                            ] : [
                                                'bg-muted',
                                                'rounded-t-2xl rounded-br-2xl'
                                            ]">
                                                <p class="text-sm">{{ message.text }}</p>
                                            </div>
                                            <p class="text-[10px] text-muted-foreground px-2"
                                                :class="message.isOwn ? 'text-right' : 'text-left'">
                                                {{ message.time }}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="flex-none border-t p-4">
                                <form @submit.prevent="sendMessage" class="flex gap-2">
                                    <Input v-model="newMessage" class="flex-1" placeholder="Введите сообщение..." />
                                    <Button type="submit" variant="secondary" size="icon" class="shrink-0">
                                        <Send class="size-4" />
                                    </Button>
                                </form>
                            </div>
                        </div>
                        <div v-else class="h-full flex items-center justify-center text-muted-foreground">
                            Выберите чат для начала общения
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </template>

    <script setup lang="ts">
    import { ref, computed, nextTick, onMounted, watch } from 'vue';
    import { Input } from '@/components/ui/input';
    import { Button } from '@/components/ui/button';
    import { Avatar, AvatarFallback } from '@/components/ui/avatar';
    import { MoreVertical, Send, X, ChevronDown, Users } from 'lucide-vue-next';
    import { ScrollArea } from '@/components/ui/scroll-area';
    import { useMediaQuery } from '@vueuse/core';

    interface Message {
        id: number;
        text: string;
        time: string;
        isOwn: boolean;
    }

    interface ChatUser {
        id: number;
        name: string;
        initials: string;
        role: string;
    }

    interface Chat {
        id: number;
        user: ChatUser;
        messages: Message[];
        unread: boolean;
        lastMessage?: Message;
    }

    const chats = ref<Chat[]>([
        {
            id: 1,
            user: { id: 1, name: 'Ольга Морозова', initials: 'ОМ', role: 'HR менеджер' },
            messages: [
                { id: 1, text: 'Здравствуйте! Хотела бы обсудить ваши карьерные планы и развитие в компании.', time: '10:30', isOwn: false },
                { id: 2, text: 'Добрый день! Да, с удовольствием обсудим', time: '10:35', isOwn: true },
            ],
            unread: true,
            lastMessage: { id: 2, text: 'Добрый день! Да, с удовольствием обсудим', time: '10:35', isOwn: true }
        },
        {
            id: 2,
            user: { id: 2, name: 'Дмитрий Соколов', initials: 'ДС', role: 'Ментор' },
            messages: [
                { id: 1, text: 'Как продвигается работа над проектом?', time: '11:45', isOwn: false },
            ],
            unread: false,
            lastMessage: { id: 1, text: 'Как продвигается работа над проектом?', time: '11:45', isOwn: false }
        },
        {
            id: 3,
            user: { id: 3, name: 'Наталья Кузнецова', initials: 'НК', role: 'HR менеджер' },
            messages: [
                { id: 1, text: 'Приглашаю вас на ежемесячную встречу команды', time: '09:15', isOwn: false },
            ],
            unread: true,
            lastMessage: { id: 1, text: 'Приглашаю вас на ежемесячную встречу команды', time: '09:15', isOwn: false }
        },
        {
            id: 4,
            user: { id: 4, name: 'Михаил Новиков', initials: 'МН', role: 'Ментор' },
            messages: [
                { id: 1, text: 'Посмотрел ваше решение последней задачи', time: '14:20', isOwn: false },
            ],
            unread: false,
            lastMessage: { id: 1, text: 'Посмотрел ваше решение последней задачи', time: '14:20', isOwn: false }
        }
    ]);

    const selectedChat = ref<Chat | null>(null);
    const newMessage = ref('');
    const searchQuery = ref('');
    const showChatList = ref(false);

    const isDesktop = useMediaQuery('(min-width: 640px)');

    const filteredChats = computed(() => {
        return chats.value.filter(chat =>
            chat.user.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            chat.user.role.toLowerCase().includes(searchQuery.value.toLowerCase())
        );
    });

    const selectChat = (chat: Chat) => {
        selectedChat.value = chat;
        chat.unread = false;
        if (!isDesktop.value) {
            showChatList.value = false;
        }
    };

    const sendMessage = () => {
        if (!selectedChat.value || !newMessage.value.trim()) return;

        const message = {
            id: Date.now(),
            text: newMessage.value,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            isOwn: true
        };

        selectedChat.value.messages.push(message);
        selectedChat.value.lastMessage = message;

        nextTick(() => {
            const viewport = document.querySelector('.scroll-area-viewport');
            if (viewport) {
                viewport.scrollTop = viewport.scrollHeight;
            }
        });

        newMessage.value = '';
    };



    const openChatWithUser = (user: ChatUser) => {
        const newChat: Chat = {
            id: Date.now(),
            user,
            messages: [],
            unread: false,
            lastMessage: undefined
        };

        chats.value.unshift(newChat);
        selectChat(newChat);
    };

    defineExpose({ openChatWithUser });

    onMounted(() => {
        const state = history.state;
        if (state?.chatUser) {
            openChatWithUser(state.chatUser);
            window.history.replaceState(null, '');
        }
    });

    const containerRef = ref<HTMLElement | null>(null);
    const showScrollDownButton = ref(false);

    const scrollToBottom = () => {
        if (containerRef.value) {
            containerRef.value.scrollTop = containerRef.value.scrollHeight;
            showScrollDownButton.value = false;
        }
    };

    const handleScroll = () => {
        if (containerRef.value) {
            const { scrollTop, scrollHeight, clientHeight } = containerRef.value;
            showScrollDownButton.value = scrollTop + clientHeight < scrollHeight - 50;
        }
    };

    watch(
        () => selectedChat.value?.messages?.length || 0,
        () => {
            nextTick(() => {
                scrollToBottom();
            });
        }
    );
    </script>

    <style scoped>
    .chat-messages {
        scroll-behavior: smooth;
        scrollbar-width: thin;
    }

    .message {
        display: flex;
        flex-direction: column;
    }

    .message-self {
        align-items: flex-end;
    }

    .message-other {
        align-items: flex-start;
    }

    .message-bubble {
        white-space: pre-wrap;
        word-break: break-word;
    }

    .message-self .message-bubble {
        background: var(--primary);
        color: var(--primary-foreground);
        border-bottom-right-radius: 5px;
    }

    .message-other .message-bubble {
        background: var(--muted);
        border-bottom-left-radius: 5px;
    }
    </style>
