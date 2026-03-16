<template>
  <div class="fixed inset-0 z-40 flex items-center justify-center bg-slate-900/40">
    <div class="w-full max-w-lg bg-white rounded-xl shadow-xl border border-slate-200">
      <header class="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
        <h2 class="text-sm font-semibold text-slate-900">
          {{ isEdit ? 'Редактирование товара' : 'Новый товар' }}
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
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block mb-1 font-medium text-slate-700">Артикул *</label>
            <input
              v-model="form.sku"
              type="text"
              class="w-full rounded-md border border-slate-300 px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
          <div>
            <label class="block mb-1 font-medium text-slate-700">Название *</label>
            <input
              v-model="form.name"
              type="text"
              class="w-full rounded-md border border-slate-300 px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block mb-1 font-medium text-slate-700">Категория</label>
            <select
              v-model="form.categoryId"
              class="w-full rounded-md border border-slate-300 px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="">Не выбрано</option>
              <option
                v-for="category in categories"
                :key="category.id"
                :value="category.id"
              >
                {{ category.name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block mb-1 font-medium text-slate-700">Поставщик</label>
            <select
              v-model="form.supplierId"
              class="w-full rounded-md border border-slate-300 px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="">Не выбрано</option>
              <option
                v-for="supplier in suppliers"
                :key="supplier.id"
                :value="supplier.id"
              >
                {{ supplier.name }}
              </option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block mb-1 font-medium text-slate-700">Цена</label>
            <div class="flex rounded-md border border-slate-300 overflow-hidden">
              <input
                v-model.number="form.price"
                type="number"
                min="0"
                step="0.01"
                class="w-full px-2 py-1.5 text-right focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              />
              <span class="inline-flex items-center px-2 bg-slate-50 text-slate-600">
                {{ currency }}
              </span>
            </div>
          </div>
          <div>
            <label class="block mb-1 font-medium text-slate-700">Остаток</label>
            <input
              v-model.number="form.stock"
              type="number"
              min="0"
              class="w-full rounded-md border border-slate-300 px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
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
import { productService } from '@/services/productService';

const props = defineProps({
  product: {
    type: Object,
    default: null,
  },
  categories: {
    type: Array,
    default: () => [],
  },
  suppliers: {
    type: Array,
    default: () => [],
  },
  currency: {
    type: String,
    default: '₽',
  },
});

const emit = defineEmits(['close', 'saved']);

const form = reactive({
  sku: '',
  name: '',
  categoryId: '',
  supplierId: '',
  price: 0,
  stock: 0,
});

const submitting = ref(false);
const error = ref('');

const isEdit = computed(() => !!props.product);

watch(
  () => props.product,
  (value) => {
    if (!value) {
      form.sku = '';
      form.name = '';
      form.categoryId = '';
      form.supplierId = '';
      form.price = 0;
      form.stock = 0;
      return;
    }
    form.sku = value.sku || '';
    form.name = value.name || '';
    form.categoryId = value.categoryId || '';
    form.supplierId = value.supplierId || '';
    form.price = value.price ?? 0;
    form.stock = value.stock ?? 0;
  },
  { immediate: true },
);

async function onSubmit() {
  error.value = '';
  if (!form.sku || !form.name) {
    error.value = 'Артикул и название обязательны для заполнения.';
    return;
  }

  submitting.value = true;
  try {
    const payload = {
      sku: form.sku,
      name: form.name,
      categoryId: form.categoryId || null,
      supplierId: form.supplierId || null,
      price: Number(form.price) || 0,
      stock: Number(form.stock) || 0,
    };

    if (isEdit.value) {
      await productService.update(props.product.id, payload);
    } else {
      await productService.create(payload);
    }

    emit('saved');
  } catch (e) {
    error.value =
      e?.response?.data?.message || 'Не удалось сохранить товар. Попробуйте позже.';
  } finally {
    submitting.value = false;
  }
}
</script>

