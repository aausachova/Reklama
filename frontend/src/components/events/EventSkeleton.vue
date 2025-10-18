<template>
    <div class="flex bg-card gap-10 rounded-xl p-6 border">
        <div class="flex flex-col items-center gap-4">
            <Skeleton class="size-[100px]" />
            <Skeleton class="h-4 w-24" />
        </div>
        <div class="flex flex-col justify-between flex-1">
            <div class="w-2/3">
                <Skeleton class="h-8 w-2/3 mb-4" />
                <Skeleton class="h-4 w-full mb-2" />
                <Skeleton class="h-4 w-full mb-2" />
                <Skeleton class="h-4 w-2/3" />
            </div>
            <div class="flex w-full justify-between items-end">
                <Skeleton class="h-4 w-32" />
                <Skeleton class="h-4 w-24" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Skeleton } from '@/components/ui/skeleton';
</script>
