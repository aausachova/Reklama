<template>
    <Line :data="chartData" :options="chartOptions" />
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Tooltip,
    Filler
} from 'chart.js';
import { Line } from 'vue-chartjs';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Tooltip,
    Filler
);

const props = defineProps<{
    period: 'month' | 'quarter'
}>();

const generateData = (days: number) => {
    const data = [];
    const date = new Date();
    for (let i = 0; i < days; i++) {
        data.unshift({
            date: new Date(date.setDate(date.getDate() - 1)).toLocaleDateString('ru', { day: 'numeric', month: 'short' }),
            value: Math.floor(Math.random() * 50) + 50
        });
    }
    return data;
};

const chartData = computed(() => {
    const data = generateData(props.period === 'month' ? 30 : 90);

    return {
        labels: data.map(item => item.date),
        datasets: [{
            fill: true,
            data: data.map(item => item.value),
            borderColor: '#3B82F6',
            backgroundColor: (context) => {
                const chart = context.chart;
                const { ctx, chartArea } = chart;
                if (!chartArea) return;

                const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
                gradient.addColorStop(0, 'rgba(59, 130, 246, 0.5)');
                gradient.addColorStop(1, 'rgba(59, 130, 246, 0)');
                return gradient;
            },
            tension: 0.4,
            pointRadius: 0
        }]
    };
});

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    resizeDelay: 200, // задержка обновления при ресайзе
    scales: {
        x: {
            grid: {
                display: false
            },
            border: {
                display: false
            },
            ticks: {
                color: '#9CA3AF',
                maxTicksLimit: 8,
                maxRotation: 0,
                callback: function (val, index) {
                    return index % 2 === 0 ? this.getLabelForValue(val) : '';
                }
            }
        },
        y: {
            display: true, // включаем отображение оси Y
            border: {
                display: false
            },
            grid: {
                drawBorder: false,
                tickLength: 0,
                lineWidth: 1,
                borderDash: [2, 4],
                stepSize: 25
            },
            ticks: {
                display: false, // скрываем числовые значения
                // Контролируем количество линий сетки
                count: 5
            }
        }
    },
    plugins: {
        legend: {
            display: false
        }
    }
};


</script>
