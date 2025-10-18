<script setup lang="ts">
import Input from '@/components/ui/input/Input.vue';
import { Search } from 'lucide-vue-next';

</script>

<template>
     <section class="px-4 pb-10">
    <div class=" mb-[44px]">
                <h1 class="text-2xl font-semibold mb-1">
                   Помощь и поддержка
                </h1>
                <p class="text-sm text-muted-foreground">
                   Центр знаний: ответы на частые вопросы, инструкции и контакт с поддержкой IT Support
                </p>
            </div>
<div class="flex items-center flex-grow min-w-[250px] relative">
        <Search class="absolute left-3 text-muted-foreground w-4 h-4" />
        <Input
 
          placeholder="Поиск вакансий"
          class="pl-9 w-full"
        />
      </div>
    </section>
</template>