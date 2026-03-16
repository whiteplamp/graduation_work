<template>
  <div class="space-y-4">
    <header class="flex items-center justify-between">
      <div>
        <h1 class="text-xl font-semibold text-slate-900">Поставщики</h1>
        <p class="text-sm text-slate-500">
          Список поставщиков с контактной информацией и возможностью редактирования.
        </p>
      </div>
      <button
        type="button"
        class="inline-flex items-center rounded-md bg-primary-600 px-3 py-2 text-xs font-medium text-white hover:bg-primary-700"
        @click="openCreate"
      >
        Добавить поставщика
      </button>
    </header>

    <section class="bg-white rounded-xl shadow-sm border border-slate-100">
      <div class="overflow-x-auto">
        <table class="min-w-full text-xs">
          <thead>
            <tr class="border-b border-slate-200 bg-slate-50 text-left text-[11px] uppercase tracking-wide text-slate-500">
              <th class="px-3 py-2">Название</th>
              <th class="px-3 py-2">Email</th>
              <th class="px-3 py-2">Телефон</th>
              <th class="px-3 py-2">Сайт</th>
              <th class="px-3 py-2">Комментарий</th>
              <th class="px-3 py-2 text-right">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="supplier in suppliers"
              :key="supplier.id"
              class="border-b border-slate-100 hover:bg-slate-50"
            >
              <td class="px-3 py-2 text-xs text-slate-800 font-medium">
                {{ supplier.name }}
              </td>
              <td class="px-3 py-2 text-xs text-slate-600">
                {{ supplier.email || '—' }}
              </td>
              <td class="px-3 py-2 text-xs text-slate-600">
                {{ supplier.phone || '—' }}
              </td>
              <td class="px-3 py-2 text-xs text-primary-600">
                <a
                  v-if="supplier.website"
                  :href="supplier.website"
                  target="_blank"
                  rel="noreferrer"
                >
                  {{ supplier.website }}
                </a>
                <span v-else>—</span>
              </td>
              <td class="px-3 py-2 text-xs text-slate-600">
                {{ supplier.note || '—' }}
              </td>
              <td class="px-3 py-2 text-right">
                <button
                  type="button"
                  class="text-xs text-primary-600 hover:text-primary-700 mr-2"
                  @click="openEdit(supplier)"
                >
                  Редактировать
                </button>
                <button
                  type="button"
                  class="text-xs text-red-600 hover:text-red-700"
                  @click="confirmDelete(supplier)"
                >
                  Удалить
                </button>
              </td>
            </tr>
            <tr v-if="!loading && suppliers.length === 0">
              <td colspan="6" class="px-3 py-4 text-center text-xs text-slate-500">
                Поставщики не найдены.
              </td>
            </tr>
            <tr v-if="loading">
              <td colspan="6" class="px-3 py-4 text-center text-xs text-slate-500">
                Загрузка...
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <SupplierModal
      v-if="modalOpen"
      :supplier="selectedSupplier"
      @close="modalOpen = false"
      @saved="handleSaved"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { supplierService } from '@/services/supplierService';
import SupplierModal from '@/components/catalog/SupplierModal.vue';

const loading = ref(false);
const suppliers = ref([]);

const modalOpen = ref(false);
const selectedSupplier = ref(null);

async function loadSuppliers() {
  loading.value = true;
  try {
    const result = await supplierService.getList();
    suppliers.value = result.items;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

function openCreate() {
  selectedSupplier.value = null;
  modalOpen.value = true;
}

function openEdit(supplier) {
  selectedSupplier.value = { ...supplier };
  modalOpen.value = true;
}

async function confirmDelete(supplier) {
  const confirmed = window.confirm(`Удалить поставщика "${supplier.name}"?`);
  if (!confirmed) return;

  try {
    await supplierService.remove(supplier.id);
    await loadSuppliers();
  } catch (error) {
    console.error(error);
  }
}

async function handleSaved() {
  modalOpen.value = false;
  await loadSuppliers();
}

onMounted(loadSuppliers);
</script>

