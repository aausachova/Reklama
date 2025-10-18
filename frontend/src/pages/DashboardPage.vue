<template>
    <section class="px-4">
        <div class="flex flex-col gap-4">
            <!-- Header -->
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                    <h1 class="text-2xl font-semibold mb-1">Аналитика проекта</h1>
                    <p class="text-sm text-muted-foreground">Статистика и показатели по всем мероприятиям</p>
                </div>
                <div class="flex items-center gap-2 w-full sm:w-auto">
                    <Button variant="outline" class="flex-1 sm:flex-initial">
                        <Download class="mr-2 size-4" />
                        Экспорт
                    </Button>
                    <Dialog v-model:open="isDialogOpen">
                        <DialogTrigger asChild>
                            <Button class="flex-1 sm:flex-initial" @click="isDialogOpen = true">
                                <Plus class="mr-2 size-4" />
                                Пригласить
                            </Button>
                        </DialogTrigger>
                        <DialogContent class="bg-card">
                            <DialogHeader>
                                <DialogTitle>Пригласить участника</DialogTitle>
                                <DialogDescription>
                                    Отправьте приглашение новому участнику. После отправки приглашения участник получит
                                    email со ссылкой для регистрации.
                                </DialogDescription>
                            </DialogHeader>
                            <div class="grid gap-4 py-4">
                                <div class="grid gap-2">
                                    <Label for="email">Email адрес</Label>
                                    <Input id="email" type="email" placeholder="email@example.com" />
                                </div>
                                <div class="grid gap-2">
                                    <Label for="role">Роль</Label>
                                    <Select>
                                        <SelectTrigger id="role">
                                            <SelectValue placeholder="Выберите роль" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="participant">Участник</SelectItem>
                                            <SelectItem value="mentor">Ментор</SelectItem>
                                            <SelectItem value="admin">Администратор</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                                <div class="grid gap-2">
                                    <Label>Доступ к проектам</Label>
                                    <div class="flex flex-wrap gap-2">
                                        <Button v-for="project in projects" :key="project.id" variant="outline"
                                            :class="{ 'bg-accent': selectedProjects.includes(project.id) }"
                                            @click="toggleProject(project.id)">
                                            {{ project.name }}
                                        </Button>
                                    </div>
                                </div>
                            </div>
                            <DialogFooter>
                                <Button variant="outline" @click="closeDialog">Отмена</Button>
                                <Button @click="inviteUser">Отправить приглашение</Button>
                            </DialogFooter>
                        </DialogContent>
                    </Dialog>
                </div>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card v-for="stat in stats" :key="stat.title">
                    <CardHeader>
                        <CardTitle class="flex items-center justify-between">
                            <span class="text-sm font-medium">{{ stat.title }}</span>
                            <component :is="stat.icon" class="size-4 text-muted-foreground" />
                        </CardTitle>
                        <CardDescription>
                            <span class="text-2xl font-bold">{{ stat.value }}</span>
                            <span :class="['text-xs ml-2', stat.trend > 0 ? 'text-green-500' : 'text-red-500']">
                                {{ stat.trend > 0 ? '+' : '' }}{{ stat.trend }}%
                            </span>
                        </CardDescription>
                    </CardHeader>
                </Card>
            </div>

            <!-- Charts Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <Card>
                    <CardHeader>
                        <CardTitle>Активность участников</CardTitle>
                        <CardDescription>Количество решений по дням</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div class="h-[300px]">
                            <AreaChart :period="'month'" />
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Распределение по навыкам</CardTitle>
                        <CardDescription>Топ технологий среди участников</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div class="h-[300px] flex gap-2">
                            <div v-for="skill in skills" :key="skill.name"
                                class="flex flex-col items-center justify-end flex-1">
                                <div class="w-full bg-primary/10 rounded-t-lg"
                                    :style="{ height: `${skill.percentage}%` }">
                                </div>
                                <span class="text-xs mt-2">{{ skill.name }}</span>
                                <span class="text-xs text-muted-foreground">{{ skill.percentage }}%</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

            <!-- Table -->
            <Card>
                <CardHeader>
                    <CardTitle>Последние участники</CardTitle>
                    <CardDescription>Список недавно присоединившихся пользователей</CardDescription>
                </CardHeader>
                <CardContent>
                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead>
                                <tr class="text-left border-b">
                                    <th class="pb-3 text-sm font-medium">Пользователь</th>
                                    <th class="pb-3 text-sm font-medium">Статус</th>
                                    <th class="pb-3 text-sm font-medium">Присоединился</th>
                                    <th class="pb-3 text-sm font-medium text-right">Действия</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="user in recentUsers" :key="user.id" class="border-b last:border-0">
                                    <td class="py-3">
                                        <div class="flex items-center gap-2">
                                            <Avatar class="size-8">
                                                <AvatarFallback>{{ user.initials }}</AvatarFallback>
                                            </Avatar>
                                            <div>
                                                <p class="text-sm font-medium">{{ user.name }}</p>
                                                <p class="text-xs text-muted-foreground">{{ user.email }}</p>
                                            </div>
                                        </div>
                                    </td>
                                    <td>
                                        <span
                                            :class="[
                                                'inline-flex items-center rounded-full px-2 py-1 text-xs',
                                                user.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700']">
                                            {{ user.status === 'active' ? 'Активный' : 'Ожидает' }}
                                        </span>
                                    </td>
                                    <td class="text-sm text-muted-foreground">{{ user.joinedAt }}</td>
                                    <td class="text-right">
                                        <Button variant="ghost" size="icon">
                                            <MoreHorizontal class="size-4" />
                                        </Button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </CardContent>
            </Card>
        </div>
    </section>
</template>

<script setup lang="ts">
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Download, Plus, Users, Trophy, Target, Briefcase, MoreHorizontal } from 'lucide-vue-next';
import AreaChart from '@/components/charts/AreaChart.vue';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';
import { ref } from 'vue';

const stats = [
    { title: 'Всего участников', value: '2,420', trend: 12, icon: Users },
    { title: 'Активные проекты', value: '24', trend: 4, icon: Briefcase },
    { title: 'Решенные кейсы', value: '842', trend: 8, icon: Trophy },
    { title: 'Конверсия', value: '24%', trend: -2, icon: Target },
];

const skills = [
    { name: 'Python', percentage: 85 },
    { name: 'JS', percentage: 65 },
    { name: 'Java', percentage: 55 },
    { name: 'C++', percentage: 45 },
    { name: 'Go', percentage: 35 },
];

const recentUsers = [
    { id: 1, name: 'Алексей Иванов', email: 'alex@example.com', status: 'active', joinedAt: '2 часа назад', initials: 'АИ' },
    { id: 2, name: 'Мария Петрова', email: 'maria@example.com', status: 'pending', joinedAt: '3 часа назад', initials: 'МП' },
    // ... другие пользователи
];

const projects = [
    { id: 1, name: 'ML Competition' },
    { id: 2, name: 'Хакатон AI' },
    { id: 3, name: 'Data Science' },
    { id: 4, name: 'Web Dev' },
];

const selectedProjects = ref<number[]>([]);
const isDialogOpen = ref(false);

const toggleProject = (id: number) => {
    const index = selectedProjects.value.indexOf(id);
    if (index === -1) {
        selectedProjects.value.push(id);
    } else {
        selectedProjects.value.splice(index, 1);
    }
};

const closeDialog = () => {
    isDialogOpen.value = false;
};

const inviteUser = () => {
    // Здесь будет логика отправки приглашения
    console.log('Приглашение отправлено');
    closeDialog();
};
</script>