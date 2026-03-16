<template>
  <div class="space-y-6">
    <section>
      <h1 class="text-2xl font-semibold text-slate-900 mb-1">
        Дашборд
      </h1>
      <p class="text-sm text-slate-500">
        Краткий обзор состояния каталога и активности загрузок.
      </p>
    </section>

    <section class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
        <p class="text-xs text-slate-500 mb-1">Всего товаров</p>
        <p class="text-2xl font-semibold text-slate-900">{{ stats.totalProducts }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
        <p class="text-xs text-slate-500 mb-1">Поставщики</p>
        <p class="text-2xl font-semibold text-slate-900">{{ stats.totalSuppliers }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
        <p class="text-xs text-slate-500 mb-1">Категории</p>
        <p class="text-2xl font-semibold text-slate-900">{{ stats.totalCategories }}</p>
      </div>
    </section>

    <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-slate-100 p-4">
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-sm font-medium text-slate-800">Недавние загрузки файлов</h2>
          <RouterLink to="/upload" class="text-xs text-primary-600 hover:text-primary-700">
            Открыть страницу загрузки
          </RouterLink>
        </div>
        <div v-if="recentUploads.length === 0" class="text-sm text-slate-500">
          Пока нет загруженных файлов.
        </div>
        <table v-else class="w-full text-xs">
          <thead>
            <tr class="text-left text-slate-500 border-b border-slate-100">
              <th class="py-2">Файл</th>
              <th class="py-2">Тип загрузки</th>
              <th class="py-2">Статус</th>
              <th class="py-2">Дата</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="file in recentUploads"
              :key="file.id"
              class="border-b border-slate-50"
            >
              <td class="py-2">{{ file.name }}</td>
              <td class="py-2">{{ file.modeLabel }}</td>
              <td class="py-2">
                <span
                  class="inline-flex items-center rounded-full px-2 py-0.5 text-[11px] font-medium"
                  :class="statusClass(file.status)"
                >
                  {{ file.statusLabel }}
                </span>
              </td>
              <td class="py-2 text-slate-500">
                {{ file.createdAt }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
        <h2 class="text-sm font-medium text-slate-800 mb-3">Быстрые метрики</h2>
        <ul class="space-y-2 text-xs text-slate-600">
          <li class="flex justify-between">
            <span>Товаров без категорий</span>
            <span class="font-medium">{{ stats.productsWithoutCategory }}</span>
          </li>
          <li class="flex justify-between">
            <span>Товаров без поставщика</span>
            <span class="font-medium">{{ stats.productsWithoutSupplier }}</span>
          </li>
          <li class="flex justify-between">
            <span>Файлов с ошибками обработки</span>
            <span class="font-medium text-red-600">{{ stats.failedUploads }}</span>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import { RouterLink } from 'vue-router';
import { dashboardService } from '@/services/dashboardService';

const stats = reactive({
  totalProducts: 0,
  totalSuppliers: 0,
  totalCategories: 0,
  productsWithoutCategory: 0,
  productsWithoutSupplier: 0,
  failedUploads: 0,
});

const recentUploads = ref([]);

function statusClass(status) {
  if (status === 'completed') {
    return 'bg-green-100 text-green-700';
  }
  if (status === 'processing') {
    return 'bg-amber-100 text-amber-700';
  }
  if (status === 'failed') {
    return 'bg-red-100 text-red-700';
  }
  return 'bg-slate-100 text-slate-600';
}

onMounted(async () => {
  try {
    const data = await dashboardService.getOverview();
    Object.assign(stats, data.stats);
    recentUploads.value = data.recentUploads;
  } catch (error) {
    // В реальном проекте показать уведомление
    console.error(error);
  }
});
</script>

