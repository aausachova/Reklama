<template>
    <div class="bg-card border rounded-lg p-6">
        <div class="flex flex-col gap-4">
            <!-- Header skeleton -->
            <div class="flex items-center gap-4">
                <Skeleton class="size-20" />
                <div class="flex-1">
                    <Skeleton class="h-6 w-2/3 mb-2" />
                    <Skeleton class="h-4 w-1/3" />
                </div>
            </div>
            
            <!-- Description skeleton -->
            <div class="space-y-2">
                <Skeleton class="h-4 w-full" />
                <Skeleton class="h-4 w-5/6" />
                <Skeleton class="h-4 w-4/6" />
            </div>

            <!-- Footer skeleton -->
            <div class="flex items-center justify-between pt-4 mt-auto">
                <Skeleton class="h-4 w-24" />
                <Skeleton class="h-4 w-20" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Skeleton } from '@/components/ui/skeleton';
</script>
