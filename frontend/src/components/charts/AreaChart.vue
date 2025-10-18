<template>
  <Line :data="chartData" :options="chartOptions" />
</template>

<script setup lang="ts">
import { computed } from "vue";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { Line } from "vue-chartjs";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend, Filler);

const stages = ["Отклик", "Скрининг", "Интервью", "Оффер", "Hire"];

const candidates = [60, 135, 95, 25, 10];
const conversion = [80, 20, 59.4, 40, 6.6];

const accentColor = "#df3053";
const accentLight = "#ff94a8"; 

const chartData = computed(() => ({
  labels: stages,
  datasets: [
    {
      label: "Количество кандидатов",
      data: candidates,
      borderColor: accentColor,
      backgroundColor: (context: any) => {
        const { chart } = context;
        const { ctx, chartArea } = chart;
        if (!chartArea) return null;
        const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
        gradient.addColorStop(0, "rgba(223, 48, 83, 1)"); 
        gradient.addColorStop(1, "rgba(223, 48, 83, 0)");
        return gradient;
      },
      tension: 0.36,
      fill: true,
      pointRadius: 2,        
      pointHoverRadius: 5,
      yAxisID: "y",
    },
    {
      label: "Конверсия (%)",
      data: conversion,
      borderColor: accentLight,
      backgroundColor: "rgba(255, 148, 168, 1)",
      tension: 0.36,
      fill: false,
      borderDash: [5, 5],
      pointRadius: 2,
      pointHoverRadius: 5,
      yAxisID: "y1",
    },
  ],
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    intersect: false,
    mode: "index" as const,
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { color: "#6B7280", font: { size: 12 } },
    },
    y: {
      type: "linear" as const,
      display: true,
      position: "left" as const,
      grid: {
        drawBorder: false,
        color: "rgba(209, 213, 219, 1)",
      },
      ticks: { color: "#9CA3AF" },
      title: { display: true, text: "Количество кандидатов", color: "#6B7280" },
    },
    y1: {
      type: "linear" as const,
      display: true,
      position: "right" as const,
      grid: { drawBorder: false, display: false },
      ticks: {
        color: "#9CA3AF",
        callback: (value: number) => `${value}%`,
      },
      title: { display: true, text: "Конверсия", color: "#6B7280" },
    },
  },
  plugins: {
    legend: {
      display: true,
      labels: {
        color: "#374151",
        usePointStyle: true,
        pointStyle: "circle",
        boxWidth: 6,   
        boxHeight: 6,
        padding: 12,
       
      },
    },
    tooltip: {
      backgroundColor: "#111827",
      titleColor: "#fff",
      bodyColor: "#d1d5db",
      borderWidth: 0,
      displayColors: true,
      callbacks: {
        label: (context: any) => {
          if (context.dataset.label === "Количество кандидатов") {
            return `Кандидаты: ${context.parsed.y}`;
          }
          if (context.dataset.label === "Конверсия (%)") {
            return `Конверсия: ${context.parsed.y}%`;
          }
          return "";
        },
      },
    },
  },
};
</script>
 