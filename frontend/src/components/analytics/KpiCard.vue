<template>
  <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
    <p class="text-xs text-slate-500 mb-1">
      {{ label }}
    </p>
    <p class="text-2xl font-semibold text-slate-900">
      {{ formattedValue }}
      <span v-if="suffix" class="text-sm font-normal text-slate-500">
        {{ suffix }}
      </span>
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  value: {
    type: Number,
    default: 0,
  },
  suffix: {
    type: String,
    default: '',
  },
});

const formattedValue = computed(() => {
  if (Number.isNaN(props.value)) return '0';
  return props.value.toLocaleString();
});
</script>

