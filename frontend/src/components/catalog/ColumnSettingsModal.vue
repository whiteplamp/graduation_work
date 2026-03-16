<template>
  <div class="fixed inset-0 z-40 flex items-center justify-center bg-slate-900/40">
    <div class="w-full max-w-sm bg-white rounded-xl shadow-xl border border-slate-200 p-5">
      <header class="mb-3 flex items-center justify-between">
        <h2 class="text-sm font-semibold text-slate-900">Отображаемые колонки</h2>
        <button
          type="button"
          class="text-slate-400 hover:text-slate-600"
          @click="$emit('close')"
        >
          ✕
        </button>
      </header>

      <div class="space-y-2 text-xs text-slate-700">
        <label class="flex items-center gap-2">
          <input
            v-model="localValue.sku"
            type="checkbox"
            class="rounded border-slate-300 text-primary-600 focus:ring-primary-500"
          />
          <span>Артикул</span>
        </label>
        <label class="flex items-center gap-2">
          <input
            v-model="localValue.name"
            type="checkbox"
            class="rounded border-slate-300 text-primary-600 focus:ring-primary-500"
          />
          <span>Название</span>
        </label>
        <label class="flex items-center gap-2">
          <input
            v-model="localValue.category"
            type="checkbox"
            class="rounded border-slate-300 text-primary-600 focus:ring-primary-500"
          />
          <span>Категория</span>
        </label>
        <label class="flex items-center gap-2">
          <input
            v-model="localValue.price"
            type="checkbox"
            class="rounded border-slate-300 text-primary-600 focus:ring-primary-500"
          />
          <span>Цена</span>
        </label>
        <label class="flex items-center gap-2">
          <input
            v-model="localValue.stock"
            type="checkbox"
            class="rounded border-slate-300 text-primary-600 focus:ring-primary-500"
          />
          <span>Остаток</span>
        </label>
        <label class="flex items-center gap-2">
          <input
            v-model="localValue.supplier"
            type="checkbox"
            class="rounded border-slate-300 text-primary-600 focus:ring-primary-500"
          />
          <span>Поставщик</span>
        </label>
      </div>

      <footer class="mt-4 flex items-center justify-end gap-2 text-xs">
        <button
          type="button"
          class="px-3 py-1.5 rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
          @click="$emit('close')"
        >
          Отмена
        </button>
        <button
          type="button"
          class="px-3 py-1.5 rounded-md bg-primary-600 text-white font-medium hover:bg-primary-700"
          @click="apply"
        >
          Применить
        </button>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue';

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['update:modelValue', 'close']);

const localValue = reactive({
  sku: true,
  name: true,
  category: true,
  price: true,
  stock: true,
  supplier: true,
});

watch(
  () => props.modelValue,
  (value) => {
    Object.assign(localValue, value);
  },
  { immediate: true },
);

function apply() {
  emit('update:modelValue', { ...localValue });
  emit('close');
}
</script>

