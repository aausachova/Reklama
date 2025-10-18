<template>
    <div class="h-full relative bg-card border rounded-lg overflow-hidden flex">
        <div class="flex flex-col py-6 px-4 justify-between w-full sm:w-1/2">
            <div class="overflow-hidden">
                <h3 class="text-2xl font-semibold mb-3 line-clamp-1">
                    Аналитика данных
                </h3>
                <p class="text-sm line-clamp-3">
                    Для специалистов, стремящихся освоить инструменты анализа, визуализации и интерпретации данных для принятия обоснованных бизнес-решений
                </p>
            </div>
            <div class="mt-auto">
                <hr class="border-t border-gray-300 mb-2" />
                <div class="flex justify-between w-full">
                    <time class="text-sm">
                        Доступен до 31.12.2025
                    </time>
                    <span class="ml-2 text-sm">
                        Уроков: 5/18
                    </span>
                </div>
                <Button size="lg" class="font-semibold mt-4 w-full sm:w-auto">
                    Продолжить курс
                </Button>
            </div>
        </div>
        <div class=" absolute top-4 right-4 py-3 px-7 bg-card border rounded-[22px] text-sm font-semibold  ">
            Extra
        </div>
        <div class="hidden sm:block sm:w-1/2 h-full bg-no-repeat bg-center bg-cover"
            style="background-image: url('/img/Card-2.png');"></div>
    </div>
</template>

<script setup lang="ts">
import { Button } from '../ui/button';
</script>

<style scoped></style>