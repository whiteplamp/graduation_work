<template>
  <div class="fixed inset-0 z-40 flex items-center justify-center bg-slate-900/40">
    <div class="w-full max-w-md bg-white rounded-xl shadow-xl border border-slate-200">
      <header class="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
        <h2 class="text-sm font-semibold text-slate-900">
          {{ isEdit ? 'Редактирование категории' : 'Новая категория' }}
        </h2>
        <button
          type="button"
          class="text-slate-400 hover:text-slate-600"
          @click="$emit('close')"
        >
          ✕
        </button>
      </header>

      <form class="px-5 py-4 space-y-3 text-xs" @submit.prevent="onSubmit">
        <div>
          <label class="block mb-1 font-medium text-slate-700">Название *</label>
          <input
            v-model="name"
            type="text"
            class="w-full rounded-md border border-slate-300 px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>

        <div v-if="parent" class="text-xs text-slate-500">
          Родительская категория: <span class="font-medium">{{ parent.name }}</span>
        </div>

        <p v-if="error" class="text-red-600 text-xs">
          {{ error }}
        </p>

        <footer class="pt-3 flex items-center justify-end gap-2 border-t border-slate-100">
          <button
            type="button"
            class="px-3 py-1.5 rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
            @click="$emit('close')"
          >
            Отмена
          </button>
          <button
            type="submit"
            class="px-3 py-1.5 rounded-md bg-primary-600 text-white font-medium hover:bg-primary-700 disabled:opacity-60"
            :disabled="submitting"
          >
            {{ submitting ? 'Сохранение...' : 'Сохранить' }}
          </button>
        </footer>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import { categoryService } from '@/services/categoryService';

const props = defineProps({
  category: {
    type: Object,
    default: null,
  },
  parent: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['close', 'saved']);

const name = ref('');
const submitting = ref(false);
const error = ref('');

const isEdit = computed(() => !!props.category);

watch(
  () => props.category,
  (value) => {
    name.value = value?.name || '';
  },
  { immediate: true },
);

async function onSubmit() {
  error.value = '';
  if (!name.value.trim()) {
    error.value = 'Введите название категории.';
    return;
  }

  submitting.value = true;
  try {
    const payload = {
      name: name.value.trim(),
      parentId: props.parent?.id ?? props.category?.parentId ?? null,
    };

    if (isEdit.value) {
      await categoryService.update(props.category.id, payload);
    } else {
      await categoryService.create(payload);
    }

    emit('saved');
  } catch (e) {
    error.value =
      e?.response?.data?.message || 'Не удалось сохранить категорию. Попробуйте позже.';
  } finally {
    submitting.value = false;
  }
}
</script>

