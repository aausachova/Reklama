<script setup lang="ts">
import LottieAnimation from '@/components/animations/LottieAnimation.vue';
const animationSrc = "/DiscussionGroupsDucks.tgs" 
import { BarChart } from "@/components/ui/chart-bar"

const data = [
  { name: "Jan", total: Math.floor(Math.random() * 2000) + 500, predicted: Math.floor(Math.random() * 2000) + 500 },
  { name: "Feb", total: Math.floor(Math.random() * 2000) + 500, predicted: Math.floor(Math.random() * 2000) + 500 },
  { name: "Mar", total: Math.floor(Math.random() * 2000) + 500, predicted: Math.floor(Math.random() * 2000) + 500 },
  { name: "Apr", total: Math.floor(Math.random() * 2000) + 500, predicted: Math.floor(Math.random() * 2000) + 500 },
  { name: "May", total: Math.floor(Math.random() * 2000) + 500, predicted: Math.floor(Math.random() * 2000) + 500 },
  { name: "Jun", total: Math.floor(Math.random() * 2000) + 500, predicted: Math.floor(Math.random() * 2000) + 500 },
  { name: "Jul", total: Math.floor(Math.random() * 2000) + 500, predicted: Math.floor(Math.random() * 2000) + 500 },
]
</script>

<template>
  <section class="max-w-3xl text-center flex flex-col flex-center mx-auto px-4 py-8">
       <LottieAnimation
        class="mx-auto"
        :src="animationSrc"
        :height="250"
        :width="250"
        renderer="svg"
      />
    <span>
        Пока тут ничего нет, но скоро появится :)
    </span>
<!-- 
    <BarChart
    :data="data"
    index="name"
    :categories="['total', 'predicted']"
    :y-formatter="(tick, i) => {
      return typeof tick === 'number'
        ? `$ ${new Intl.NumberFormat('us').format(tick).toString()}`
        : ''
    }"
  /> -->
</section>
    </template>