<template>
    <Dialog :open="open" @update:open="$emit('update:open', $event)">
        <DialogContent class="sm:max-w-[600px]">
            <DialogHeader>
                <DialogTitle>{{ course?.title }}</DialogTitle>
                <DialogDescription>{{ course?.description }}</DialogDescription>
            </DialogHeader>

            <div class="space-y-6">
                <div>
                    <h4 class="text-sm font-medium mb-2">Требования к курсу</h4>
                    <ul class="list-disc pl-4 space-y-1">
                        <li v-for="req in course?.requirements" :key="req" class="text-sm text-muted-foreground">
                            {{ req }}
                        </li>
                    </ul>
                </div>

                <div>
                    <h4 class="text-sm font-medium mb-2">Чему вы научитесь</h4>
                    <ul class="list-disc pl-4 space-y-1">
                        <li v-for="item in course?.whatYouWillLearn" :key="item" class="text-sm text-muted-foreground">
                            {{ item }}
                        </li>
                    </ul>
                </div>
            </div>


        </DialogContent>
    </Dialog>
</template>

<script setup lang="ts">
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import type { Course } from '@/types/course';

defineProps<{
    open: boolean;
    course: Course | null;
}>();

defineEmits<{
    'update:open': [value: boolean];
}>();
</script>
