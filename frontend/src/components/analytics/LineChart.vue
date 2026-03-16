<template>
  <div class="w-full h-40 flex items-center justify-center">
    <div v-if="!points.length" class="text-xs text-slate-500">
      Нет данных для отображения.
    </div>
    <svg
      v-else
      viewBox="0 0 100 40"
      class="w-full h-full overflow-visible"
      preserveAspectRatio="none"
    >
      <defs>
        <linearGradient id="line-fill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.35" />
          <stop offset="100%" stop-color="#3b82f6" stop-opacity="0" />
        </linearGradient>
      </defs>

      <path
        :d="areaPath"
        fill="url(#line-fill)"
      />

      <polyline
        :points="polylinePoints"
        fill="none"
        stroke="#2563eb"
        stroke-width="1.5"
        stroke-linejoin="round"
        stroke-linecap="round"
      />
    </svg>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  points: {
    type: Array,
    default: () => [],
  },
});

const normalized = computed(() => {
  if (!props.points.length) return [];
  const values = props.points.map((p) => Number(p.value) || 0);
  const max = Math.max(...values);
  const min = Math.min(...values);
  const range = max - min || 1;

  return values.map((v, index) => {
    const x = (index / Math.max(props.points.length - 1, 1)) * 100;
    const y = 5 + (1 - (v - min) / range) * 30;
    return { x, y };
  });
});

const polylinePoints = computed(() =>
  normalized.value.map((p) => `${p.x},${p.y}`).join(' '),
);

const areaPath = computed(() => {
  if (!normalized.value.length) return '';
  const first = normalized.value[0];
  const last = normalized.value[normalized.value.length - 1];
  const line = normalized.value.map((p) => `L ${p.x} ${p.y}`).join(' ');
  return `M ${first.x} 40 ${line} L ${last.x} 40 Z`;
});
</script>

