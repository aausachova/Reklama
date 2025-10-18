<script setup lang="ts">
import { ref, onMounted } from "vue"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { TrendingUp } from "lucide-vue-next"

const statCards = [
  { title: "Кадровый резерв вуза", value: 128 },
  { title: "Активные вакансии", value: 42 },
  { title: "Отклики соискателей", value: 314 },
  { title: "Среднее время ответа (SLA)", value: "2.4 дня", trend: "+12%" },
]

const candidates = ref<any[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    const res = await fetch("/api/candidate/")
    if (!res.ok) throw new Error(`Ошибка загрузки: ${res.status}`)
    const data = await res.json()
    candidates.value = data
  } catch (err: any) {
    error.value = err.message || "Не удалось загрузить данные"
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="p-6 space-y-8">
    <!-- 🧭 Заголовок -->
    <h1 class="text-2xl font-semibold">Витрина вакансий</h1>

    <!-- 📊 Карточки статистики -->
    <div class="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
      <Card
        v-for="(item, i) in statCards"
        :key="i"
        class="flex flex-col justify-center rounded-2xl"
      >
        <CardHeader class="flex justify-between items-center">
          <CardTitle class="text-xs text-primary">{{ item.title }}</CardTitle>
          <Badge
            v-if="item.title.includes('SLA')"
            variant="secondary"
            class="flex items-center gap-1"
          >
            <TrendingUp class="w-4 h-4" />
            {{ item.trend }}
          </Badge>
        </CardHeader>
        <CardContent>
          <p class="text-5xl font-semibold text-foreground">{{ item.value }}</p>
        </CardContent>
      </Card>
    </div>

    <!-- 📋 Таблица кандидатов -->
    <Card class="rounded-2xl">
      <CardContent>
        <div v-if="loading" class="text-muted-foreground text-sm p-4">
          Загрузка данных...
        </div>
        <div v-else-if="error" class="text-destructive text-sm p-4">
          {{ error }}
        </div>
        <div v-else>
          <Table class="min-w-full border-separate border-spacing-y-2">
            <TableHeader>
              <TableRow>
                <TableHead>ФИО</TableHead>
                <TableHead>Направление</TableHead>
                <TableHead>Контактные данные</TableHead>
                <TableHead class="text-right">Решение по кандидату</TableHead>
              </TableRow>
            </TableHeader>

            <TableBody>
              <TableRow
                v-for="(c, i) in candidates"
                :key="c.id || i"
                class="bg-card hover:bg-muted/30 transition"
              >
                <TableCell class="font-medium">{{ c.full_name }}</TableCell>
                <TableCell>{{ c.direction }}</TableCell>
                <TableCell class="text-sm text-muted-foreground">
                  <div>{{ c.email }}</div>
                  <div>{{ c.phone }}</div>
                </TableCell>
                <TableCell class="text-right">
                  <DropdownMenu>
                    <DropdownMenuTrigger as-child>
                      <Button variant="outline" size="sm">Выбрать</Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem>Одобрить</DropdownMenuItem>
                      <DropdownMenuItem>Отклонить</DropdownMenuItem>
                      <DropdownMenuItem>В архив</DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>

          <p v-if="!candidates.length" class="text-sm text-muted-foreground p-4">
            Нет доступных кандидатов
          </p>
        </div>
      </CardContent>
    </Card>
  </section>
</template>
