<template>
  <div class="fixed inset-0 z-40 flex items-center justify-center bg-slate-900/40">
    <div class="w-full max-w-md bg-white rounded-xl shadow-xl border border-slate-200">
      <header class="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
        <h2 class="text-sm font-semibold text-slate-900">
          {{ isEdit ? 'Редактирование поставщика' : 'Новый поставщик' }}
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
            v-model="form.name"
            type="text"
            class="w-full rounded-md border border-slate-300 px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block mb-1 font-medium text-slate-700">Email</label>
            <input
              v-model="form.email"
              type="email"
              class="w-full rounded-md border border-slate-300 px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
          <div>
            <label class="block mb-1 font-medium text-slate-700">Телефон</label>
            <input
              v-model="form.phone"
              type="text"
              class="w-full rounded-md border border-slate-300 px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
        </div>

        <div>
          <label class="block mb-1 font-medium text-slate-700">Сайт</label>
          <input
            v-model="form.website"
            type="url"
            class="w-full rounded-md border border-slate-300 px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>

        <div>
          <label class="block mb-1 font-medium text-slate-700">Комментарий</label>
          <textarea
            v-model="form.note"
            rows="2"
            class="w-full rounded-md border border-slate-300 px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
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
import { computed, reactive, ref, watch } from 'vue';
import { supplierService } from '@/services/supplierService';

const props = defineProps({
  supplier: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['close', 'saved']);

const form = reactive({
  name: '',
  email: '',
  phone: '',
  website: '',
  note: '',
});

const submitting = ref(false);
const error = ref('');

const isEdit = computed(() => !!props.supplier);

watch(
  () => props.supplier,
  (value) => {
    form.name = value?.name || '';
    form.email = value?.email || '';
    form.phone = value?.phone || '';
    form.website = value?.website || '';
    form.note = value?.note || '';
  },
  { immediate: true },
);

async function onSubmit() {
  error.value = '';
  if (!form.name.trim()) {
    error.value = 'Введите название поставщика.';
    return;
  }

  submitting.value = true;
  try {
    const payload = { ...form };
    if (isEdit.value) {
      await supplierService.update(props.supplier.id, payload);
    } else {
      await supplierService.create(payload);
    }
    emit('saved');
  } catch (e) {
    error.value =
      e?.response?.data?.message ||
      'Не удалось сохранить поставщика. Попробуйте позже.';
  } finally {
    submitting.value = false;
  }
}
</script>

