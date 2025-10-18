<template>
    <section class="px-4 py-6">
        <div class="w-full max-w-[700px] mx-auto flex flex-col space-y-4">
            <h1 class="text-2xl font-bold">Добавление позиции</h1>

            <!-- Вкладки -->
            <div class="flex border-b border-muted/50 mb-4">
                <button
                    :class="['px-4 py-2 font-semibold', activeTab === 'vacancy' ? 'border-b-2 border-primary text-primary' : 'text-muted-foreground']"
                    @click="activeTab = 'vacancy'">
                    Вакансия
                </button>
                <button
                    :class="['px-4 py-2 font-semibold', activeTab === 'internship' ? 'border-b-2 border-primary text-primary' : 'text-muted-foreground']"
                    @click="activeTab = 'internship'">
                    Стажировка
                </button>
            </div>

            <!-- Контент вкладок -->
            <div v-if="activeTab === 'vacancy'">
                <form @submit.prevent="onSubmitVacancy" class="space-y-4">
                    <FormField v-slot="{ componentField }" name="title">
                        <FormItem>
                            <FormLabel>Название вакансии</FormLabel>
                            <FormControl>
                                <Input v-bind="componentField" placeholder="Введите название вакансии"
                                    class="h-10 !bg-card" />
                            </FormControl>
                            <FormMessage class="text-xs text-destructive" />
                        </FormItem>
                    </FormField>

                    <FormField v-slot="{ componentField }" name="company">
                        <FormItem>
                            <FormLabel>Название компании</FormLabel>
                            <FormControl>
                                <Input v-bind="componentField" placeholder="Введите название компании"
                                    class="h-10 !bg-card" />
                            </FormControl>
                            <FormMessage class="text-xs text-destructive" />
                        </FormItem>
                    </FormField>

                    <FormField v-slot="{ componentField }" name="specialty">
                        <FormItem>
                            <FormLabel>Специальность</FormLabel>
                            <FormControl>
                                <Input v-bind="componentField" placeholder="Введите специальность"
                                    class="h-10 !bg-card" />
                            </FormControl>
                            <FormMessage class="text-xs text-destructive" />
                        </FormItem>
                    </FormField>

                    <FormField v-slot="{ componentField }" name="platform">
                        <FormItem>
                            <FormLabel>Площадка</FormLabel>
                            <FormControl>
                                <Input v-bind="componentField" placeholder="Введите площадку" class="h-10 !bg-card" />
                            </FormControl>
                            <FormMessage class="text-xs text-destructive" />
                        </FormItem>
                    </FormField>

                    <FormField v-slot="{ componentField }" name="salary" :value-as-number="true">
                        <FormItem>
                            <FormLabel>Заработная плата</FormLabel>
                            <FormControl>
                                <Input v-bind="componentField" type="number" placeholder="Введите ЗП"
                                    class="h-10 !bg-card" />
                            </FormControl>
                            <FormMessage class="text-xs text-destructive" />
                        </FormItem>
                    </FormField>

                    <FormField v-slot="{ componentField }" name="address">
                        <FormItem>
                            <FormLabel>Адрес</FormLabel>
                            <FormControl>
                                <Input v-bind="componentField" placeholder="Введите адрес" class="h-10 !bg-card" />
                            </FormControl>
                            <FormMessage class="text-xs text-destructive" />
                        </FormItem>
                    </FormField>

                    <FormField v-slot="{ componentField }" name="description">
                        <FormItem>
                            <FormLabel>Описание</FormLabel>
                            <FormControl>
                                <textarea v-bind="componentField" placeholder="Описание вакансии"
                                    class="w-full h-24 p-2 !bg-card rounded-md"></textarea>
                            </FormControl>
                            <FormMessage class="text-xs text-destructive" />
                        </FormItem>
                    </FormField>

                    <Button size="lg" type="submit" class="w-full">Создать вакансию</Button>
                </form>
            </div>

            <div v-if="activeTab === 'internship'">
                <form @submit.prevent="onSubmitInternship" class="space-y-4">
                    <FormField v-slot="{ componentField }" name="title">
                        <FormItem>
                            <FormLabel>Название стажировки</FormLabel>
                            <FormControl>
                                <Input v-bind="componentField" placeholder="Введите название стажировки"
                                    class="h-10 !bg-card" />
                            </FormControl>
                            <FormMessage class="text-xs text-destructive" />
                        </FormItem>
                    </FormField>

                    <FormField v-slot="{ componentField }" name="company">
                        <FormItem>
                            <FormLabel>Компания</FormLabel>
                            <FormControl>
                                <Input v-bind="componentField" placeholder="Введите компанию" class="h-10 !bg-card" />
                            </FormControl>
                            <FormMessage class="text-xs text-destructive" />
                        </FormItem>
                    </FormField>

                    <FormField v-slot="{ componentField }" name="specialty">
                        <FormItem>
                            <FormLabel>Специальность</FormLabel>
                            <FormControl>
                                <Input v-bind="componentField" placeholder="Введите специальность"
                                    class="h-10 !bg-card" />
                            </FormControl>
                            <FormMessage class="text-xs text-destructive" />
                        </FormItem>
                    </FormField>

                    <FormField v-slot="{ componentField }" name="duration" :value-as-number="true">
                        <FormItem>
                            <FormLabel>Длительность (в месяцах)</FormLabel>
                            <FormControl>
                                <Input v-bind="componentField" type="number"
                                    placeholder="Введите длительность стажировки" class="h-10 !bg-card" />
                            </FormControl>
                            <FormMessage class="text-xs text-destructive" />
                        </FormItem>
                    </FormField>


                    <FormField v-slot="{ componentField }" name="address">
                        <FormItem>
                            <FormLabel>Адрес</FormLabel>
                            <FormControl>
                                <Input v-bind="componentField" placeholder="Введите адрес" class="h-10 !bg-card" />
                            </FormControl>
                            <FormMessage class="text-xs text-destructive" />
                        </FormItem>
                    </FormField>

                    <FormField v-slot="{ componentField }" name="description">
                        <FormItem>
                            <FormLabel>Описание</FormLabel>
                            <FormControl>
                                <textarea v-bind="componentField" placeholder="Описание стажировки"
                                    class="w-full h-24 p-2 !bg-card rounded-md"></textarea>
                            </FormControl>
                            <FormMessage class="text-xs text-destructive" />
                        </FormItem>
                    </FormField>

                    <Button size="lg" type="submit" class="w-full">Создать стажировку</Button>
                </form>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/components/ui/form'

const activeTab = ref<'vacancy' | 'internship'>('vacancy')

const onSubmitVacancy = (values: any) => {
    console.log('Создана вакансия:', values)
    alert('Вакансия создана! Проверьте консоль.')
}

const onSubmitInternship = (values: any) => {
    console.log('Создана стажировка:', values)
    alert('Стажировка создана! Проверьте консоль.')
}
</script>
