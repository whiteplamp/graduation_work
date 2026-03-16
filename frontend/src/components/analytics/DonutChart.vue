<template>
  <div class="flex items-center gap-3">
    <div class="relative w-24 h-24">
      <svg viewBox="0 0 32 32" class="w-full h-full -rotate-90">
        <circle
          cx="16"
          cy="16"
          r="14"
          fill="none"
          stroke="#e5e7eb"
          stroke-width="4"
        />
        <circle
          v-for="(segment, index) in segments"
          :key="index"
          cx="16"
          cy="16"
          r="14"
          fill="none"
          :stroke="segment.color"
          stroke-width="4"
          stroke-linecap="round"
          :stroke-dasharray="segment.length + ' ' + (100 - segment.length)"
          :stroke-dashoffset="segment.offset"
        />
      </svg>
      <div
        class="absolute inset-0 flex items-center justify-center text-[10px] font-medium text-slate-700 rotate-90"
      >
        {{ totalValue }}
      </div>
    </div>

    <ul class="flex-1 space-y-1 text-[11px] text-slate-700">
      <li
        v-for="(item, index) in items"
        :key="item.id || item.name || index"
        class="flex items-center justify-between gap-2"
      >
        <div class="flex items-center gap-2">
          <span
            class="w-2 h-2 rounded-full"
            :style="{ backgroundColor: colorPalette[index % colorPalette.length] }"
          />
          <span class="truncate">{{ item.name || item.label }}</span>
        </div>
        <span class="text-slate-500">
          {{ item.value }} ({{ share(item) }}%)
        </span>
      </li>
      <li v-if="!items.length" class="text-slate-500">
        Нет данных.
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
});

const colorPalette = ['#3b82f6', '#22c55e', '#f97316', '#e11d48', '#a855f7'];

const totalValue = computed(() =>
  props.items.reduce((sum, item) => sum + (Number(item.value) || 0), 0),
);

const segments = computed(() => {
  if (!props.items.length || !totalValue.value) return [];

  let offset = 25;
  return props.items.map((item, index) => {
    const length = ((Number(item.value) || 0) / totalValue.value) * 100;
    const segment = {
      length,
      offset,
      color: colorPalette[index % colorPalette.length],
    };
    offset -= length;
    return segment;
  });
});

function share(item) {
  if (!totalValue.value) return 0;
  return Math.round(((Number(item.value) || 0) / totalValue.value) * 100);
}
</script>

