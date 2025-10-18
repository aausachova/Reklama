<template>
    <section class="px-4">
        <div class="flex flex-col gap-4">
            <!-- Header with Create Event Button -->
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                    <h1 class="text-2xl font-semibold mb-1">Аналитика участников</h1>
                    <p class="text-sm text-muted-foreground">Анализ активности и управление участниками</p>
                </div>
                <div class="flex items-center gap-2 w-full sm:w-auto">
                    <Button @click="showCreateEventDialog = true">
                        <Plus class="mr-2 size-4" />
                        Создать мероприятие
                    </Button>
                </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card>
                    <CardHeader>
                        <CardTitle class="text-sm font-medium">Активные участники</CardTitle>
                        <CardDescription>
                            <span class="text-2xl font-bold">234</span>
                            <span class="text-green-500 text-xs ml-2">+12%</span>
                        </CardDescription>
                    </CardHeader>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle class="text-sm font-medium">Средняя активность</CardTitle>
                        <CardDescription>
                            <span class="text-2xl font-bold">4.2</span>
                            <span class="text-xs ml-2">часа в день</span>
                        </CardDescription>
                    </CardHeader>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle class="text-sm font-medium">Успешные собеседования</CardTitle>
                        <CardDescription>
                            <span class="text-2xl font-bold">85%</span>
                            <span class="text-green-500 text-xs ml-2">+5%</span>
                        </CardDescription>
                    </CardHeader>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle class="text-sm font-medium">Общий прогресс</CardTitle>
                        <CardDescription class="flex items-center gap-2">
                            <Progress :model-value="75" class="flex-1 " />
                            <span class="text-sm font-medium">75%</span>
                        </CardDescription>
                    </CardHeader>
                </Card>
            </div>



            <Dialog v-model:open="showCreateEventDialog">
                <DialogContent class="max-w-5xl bg-card">
                    <DialogHeader>
                        <DialogTitle>Создание мероприятия</DialogTitle>
                        <DialogDescription>
                            Настройте параметры нового мероприятия
                        </DialogDescription>
                    </DialogHeader>

                    <Tabs defaultValue="general" class="w-full">
                        <TabsList class="grid w-full grid-cols-3">
                            <TabsTrigger value="general">Основное</TabsTrigger>
                            <TabsTrigger value="requirements">Требования</TabsTrigger>
                            <TabsTrigger value="schedule">Расписание</TabsTrigger>
                        </TabsList>

                        <TabsContent value="general">
                            <div class="grid grid-cols-2 gap-4">
                                <div class="space-y-2">
                                    <Label>Название мероприятия</Label>
                                    <Input v-model="eventForm.title" placeholder="Введите название" />
                                </div>
                                <div class="space-y-2">
                                    <Label>Направление</Label>
                                    <Select v-model="eventForm.category">
                                        <SelectTrigger>
                                            <SelectValue placeholder="Выберите направление" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="ai">Искусственный интеллект</SelectItem>
                                            <SelectItem value="web">Веб-разработка</SelectItem>
                                            <SelectItem value="mobile">Мобильная разработка</SelectItem>
                                            <SelectItem value="data">Данные</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                                <div class="col-span-2 space-y-2">
                                    <Label>Описание</Label>
                                    <Textarea class=" max-h-56  " v-model="eventForm.description"
                                        placeholder="Опишите мероприятие" />
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="requirements" class="space-y-4">
                            <div class="space-y-4">

                                <div class="space-y-2">
                                    <Label>Максимальный размер команды</Label>
                                    <NumberField v-model="eventForm.maxTeamSize">
                                        <NumberFieldContent>
                                            <NumberFieldDecrement />
                                            <NumberFieldInput />
                                            <NumberFieldIncrement />
                                        </NumberFieldContent>
                                    </NumberField>
                                </div>
                                <div class="space-y-2">
                                    <Label>Максимальное количество решений</Label>
                                    <NumberField v-model="eventForm.maxSolutions" >
                                        <NumberFieldContent>
                                            <NumberFieldDecrement />
                                            <NumberFieldInput />
                                            <NumberFieldIncrement />
                                        </NumberFieldContent>
                                    </NumberField>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="schedule" class="space-y-4">
                            <div class="grid grid-cols-1 gap-4">
                                <div class="space-y-2">
                                    <Label>Дата начала регистрации</Label>
                                    <Input type="datetime-local" v-model="eventForm.registrationStart" />
                                </div>
                                <div class="space-y-2">
                                    <Label>Дата окончания регистрации</Label>
                                    <Input type="datetime-local" v-model="eventForm.registrationEnd" />
                                </div>
                                <div class="space-y-2">
                                    <Label>Дата начала мероприятия</Label>
                                    <Input type="datetime-local" v-model="eventForm.eventStart" />
                                </div>
                                <div class="space-y-2">
                                    <Label>Дата окончания мероприятия</Label>
                                    <Input type="datetime-local" v-model="eventForm.eventEnd" />
                                </div>
                            </div>
                        </TabsContent>
                    </Tabs>

                    <DialogFooter>
                        <Button variant="outline" @click="showCreateEventDialog = false">Отмена</Button>
                        <Button @click="createEvent">Создать мероприятие</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
                <Card class="lg:col-span-2">
                    <CardHeader class="flex flex-row items-center justify-between">
                        <div>
                            <CardTitle>Топ участников</CardTitle>
                            <CardDescription>По уровню активности и достижениям</CardDescription>
                        </div>
                        <Select v-model="selectedSort">
                            <SelectTrigger class="w-[180px]">
                                <SelectValue placeholder="Сортировка" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="activity">По активности</SelectItem>
                                <SelectItem value="achievements">По достижениям</SelectItem>
                                <SelectItem value="level">По уровню</SelectItem>
                            </SelectContent>
                        </Select>
                    </CardHeader>
                    <CardContent>
                        <div class="space-y-6">
                            <div v-for="user in topUsers" :key="user.id"
                                class="flex flex-col sm:flex-row sm:items-center justify-between p-3 rounded-lg hover:bg-muted transition-colors gap-4 cursor-pointer"
                                @click="openUserDetails(user.id)">
                                <div class="flex items-center gap-3">
                                    <Avatar class="size-10">
                                        <AvatarFallback class="bg-card border">{{ user.initials }}</AvatarFallback>
                                    </Avatar>
                                    <div class="min-w-0 flex-1">
                                        <div class="flex flex-col sm:flex-row sm:items-center gap-2">
                                            <p class="font-medium truncate">{{ user.name }}</p>
                                            <Badge variant="secondary" class="w-fit">
                                                Level {{ user.level }}
                                            </Badge>
                                        </div>
                                        <div class="flex flex-wrap gap-4 text-sm text-muted-foreground mt-1">
                                            <div class="flex items-center gap-1">
                                                <Trophy class="size-4 flex-shrink-0" />
                                                <span>{{ user.achievements }} достижений</span>
                                            </div>
                                            <div class="flex items-center gap-1">
                                                <Clock class="size-4 flex-shrink-0" />
                                                <span>{{ user.activeTime }} часов</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <Button class="w-full sm:w-auto" @click.stop="openChat(user)">
                                    <MessageSquare class="mr-2 size-4" />
                                    Связаться
                                </Button>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Активность по кейсам</CardTitle>
                        <CardDescription>Распределение участников</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div class="space-y-4">
                            <div v-for="kase in cases" :key="kase.name" class="space-y-2">
                                <div class="flex justify-between text-sm">
                                    <span class="font-medium">{{ kase.name }}</span>
                                    <Badge variant="outline">{{ kase.users }} участников</Badge>
                                </div>
                                <Progress :model-value="(kase.users / totalUsers) * 100" />
                                <div class="flex justify-between text-xs text-muted-foreground">
                                    <span>Активных: {{ kase.active }}</span>
                                    <span>Завершили: {{ kase.completed }}</span>
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    </section>

    <Dialog v-model:open="showUserDetails">
        <DialogContent class="max-w-3xl bg-card">
            <DialogHeader>
                <DialogTitle>Профиль участника</DialogTitle>
                <DialogDescription>
                    Подробная информация об участнике и его достижениях
                </DialogDescription>
            </DialogHeader>

            <Tabs v-if="selectedUser" defaultValue="info" class="w-full">
                <TabsList class="w-full">
                    <TabsTrigger value="info">Общая информация</TabsTrigger>
                    <TabsTrigger value="history">История участия</TabsTrigger>
                </TabsList>

                <TabsContent value="info" class="space-y-4">
                    <div class="flex items-start gap-4">
                        <Avatar class="size-16">
                            <AvatarFallback class="text-lg">
                                {{ selectedUser.initials }}
                            </AvatarFallback>
                        </Avatar>
                        <div>
                            <h3 class="text-xl font-semibold">{{ selectedUser.name }}</h3>
                            <p class="text-sm text-muted-foreground">
                                Зарегистрирован: {{ selectedUser.registrationDate }}
                            </p>
                            <p class="text-sm text-muted-foreground">
                                Последняя активность: {{ selectedUser.lastActive }}
                            </p>
                        </div>
                    </div>

                    <div class="space-y-2">
                        <h4 class="font-medium">Технический стек</h4>
                        <div class="flex flex-wrap gap-2">
                            <Badge v-for="tech in selectedUser.stack" :key="tech" variant="secondary">
                                {{ tech }}
                            </Badge>
                        </div>
                    </div>

                    <div class="space-y-2">
                        <h4 class="font-medium">Статистика</h4>
                        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                            <div class="space-y-1">
                                <p class="text-sm text-muted-foreground">Уровень</p>
                                <p class="text-xl font-semibold">{{ selectedUser.level }}</p>
                            </div>
                            <div class="space-y-1">
                                <p class="text-sm text-muted-foreground">Достижения</p>
                                <p class="text-xl font-semibold">{{ selectedUser.achievements }}</p>
                            </div>
                            <div class="space-y-1">
                                <p class="text-sm text-muted-foreground">Активность</p>
                                <p class="text-xl font-semibold">{{ selectedUser.activeTime }}ч</p>
                            </div>
                        </div>
                    </div>
                </TabsContent>

                <TabsContent value="history">
                    <div class="space-y-4">
                        <div v-for="project in selectedUser.projectsHistory" :key="project.id"
                            class="flex items-center justify-between p-4 border rounded-lg">
                            <div>
                                <h4 class="font-medium">{{ project.name }}</h4>
                                <p class="text-sm text-muted-foreground">{{ project.date }}</p>
                            </div>
                            <div class="flex items-center gap-4">
                                <Badge v-if="project.rating" variant="outline">
                                    {{ project.rating }}/10
                                </Badge>
                                <Badge :class="getStatusColor(project.status)">
                                    {{ project.status === 'completed' ? 'Завершен' :
                                        project.status === 'in_progress' ? 'В процессе' : 'Отменен' }}
                                </Badge>
                            </div>
                        </div>
                    </div>
                </TabsContent>
            </Tabs>
        </DialogContent>
    </Dialog>
</template>

<script setup lang="ts">
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Clock, MessageSquare, Trophy } from 'lucide-vue-next';
import { Select } from '@/components/ui/select';
import SelectTrigger from '@/components/ui/select/SelectTrigger.vue';
import SelectValue from '@/components/ui/select/SelectValue.vue';
import SelectContent from '@/components/ui/select/SelectContent.vue';
import SelectItem from '@/components/ui/select/SelectItem.vue';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { Plus } from 'lucide-vue-next';
import { NumberField, NumberFieldContent, NumberFieldDecrement, NumberFieldIncrement, NumberFieldInput } from '@/components/ui/number-field';
import { Input } from '@/components/ui/input';
import Label from '@/components/ui/label/Label.vue';
import { Textarea } from '@/components/ui/textarea';

interface User {
    id: number;
    name: string;
    initials: string;
    achievements: number;
    level: number;
    activeTime: number;
    status: string;
}

interface UserHistory {
    id: number;
    name: string;
    date: string;
    status: 'completed' | 'in_progress' | 'abandoned';
    rating?: number;
}

interface UserDetails extends User {
    stack: string[];
    registrationDate: string;
    lastActive: string;
    projectsHistory: UserHistory[];
}

const selectedSort = ref('activity');

const users: User[] = [
    {
        id: 1,
        name: 'Иван Королев',
        initials: 'ИК',
        achievements: 15,
        level: 5,
        activeTime: 127,
        status: 'active'
    },
    {
        id: 2,
        name: 'Екатерина Белова',
        initials: 'ЕБ',
        achievements: 8,
        level: 3,
        activeTime: 95,
        status: 'active'
    },
    {
        id: 3,
        name: 'Артем Захаров',
        initials: 'АЗ',
        achievements: 12,
        level: 4,
        activeTime: 145,
        status: 'active'
    },
];

const topUsers = computed(() => {
    return [...users].sort((a, b) => {
        switch (selectedSort.value) {
            case 'activity':
                return b.activeTime - a.activeTime;
            case 'achievements':
                return b.achievements - a.achievements;
            case 'level':
                return b.level - a.level;
            default:
                return 0;
        }
    });
});

const totalUsers = 234;

const cases = [
    {
        name: 'ML Competition',
        users: 125,
        active: 89,
        completed: 36
    },
    {
        name: 'Web Development',
        users: 98,
        active: 67,
        completed: 31
    },
    {
        name: 'Data Science',
        users: 76,
        active: 45,
        completed: 31
    },
    {
        name: 'AI Challenge',
        users: 45,
        active: 28,
        completed: 17
    }
];

const selectedUser = ref<UserDetails | null>(null);
const showUserDetails = ref(false);
const showCreateEventDialog = ref(false);



const eventForm = ref({
    title: '',
    description: '',
    category: '',
    maxTeamSize: 5,
    maxSolutions: 100,
    registrationStart: '',
    registrationEnd: '',
    eventStart: '',
    eventEnd: '',
    stages: [] as Array<{ name: string; date: string }>,
});




const createEvent = () => {
    console.log(eventForm.value);
    showCreateEventDialog.value = false;
};

const userDetails: Record<number, UserDetails> = {
    1: {
        id: 1,
        name: 'Иван Королев',
        initials: 'ИК',
        achievements: 15,
        level: 5,
        activeTime: 127,
        status: 'active',
        stack: ['Python', 'PyTorch', 'TensorFlow', 'scikit-learn', 'pandas'],
        registrationDate: '15 января 2024',
        lastActive: '2 часа назад',
        projectsHistory: [
            { id: 1, name: 'ML Competition', date: '20.02.2024', status: 'completed', rating: 9.5 },
            { id: 2, name: 'Data Science Challenge', date: '15.01.2024', status: 'completed', rating: 8.7 },
            { id: 3, name: 'AI Hackathon', date: '01.03.2024', status: 'in_progress' },
        ]
    },
    2: {
        id: 2,
        name: 'Екатерина Белова',
        initials: 'ЕБ',
        achievements: 8,
        level: 3,
        activeTime: 95,
        status: 'active',
        stack: ['JavaScript', 'React', 'Node.js'],
        registrationDate: '10 февраля 2024',
        lastActive: '1 день назад',
        projectsHistory: [
            { id: 1, name: 'Web Development', date: '18.02.2024', status: 'completed', rating: 9.0 },
            { id: 2, name: 'ML Competition', date: '20.02.2024', status: 'in_progress' },
        ]
    },
    3: {
        id: 3,
        name: 'Артем Захаров',
        initials: 'АЗ',
        achievements: 12,
        level: 4,
        activeTime: 145,
        status: 'active',
        stack: ['Java', 'Spring', 'Hibernate', 'MySQL'],
        registrationDate: '5 февраля 2024',
        lastActive: '3 часа назад',
        projectsHistory: [
            { id: 1, name: 'AI Challenge', date: '25.02.2024', status: 'completed', rating: 8.5 },
            { id: 2, name: 'Data Science', date: '28.02.2024', status: 'in_progress' },
        ]
    },
};

const openUserDetails = (userId: number) => {
    selectedUser.value = userDetails[userId];
    showUserDetails.value = true;
};

const router = useRouter();

const openChat = (user: User) => {
    router.push({
        name: 'chat',
        replace: true,
        state: {
            chatUser: {
                id: Date.now(),
                name: user.name,
                initials: user.initials,
                role: 'Участник'
            }
        }
    });
};

const getStatusColor = (status: string) => {
    switch (status) {
        case 'completed': return 'text-green-600 bg-green-100';
        case 'in_progress': return 'text-blue-600 bg-blue-100';
        case 'abandoned': return 'text-red-600 bg-red-100';
        default: return '';
    }
};
</script>
