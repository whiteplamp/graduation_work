<template>
  <div class="space-y-4">
    <header class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
      <div>
        <h1 class="text-xl font-semibold text-slate-900">Аналитика</h1>
        <p class="text-sm text-slate-500">
          Ключевые показатели, динамика продаж и структура каталога.
        </p>
      </div>
      <div class="flex items-center gap-2 text-xs">
        <select
          v-model="periodPreset"
          class="rounded-md border border-slate-300 px-2 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          @change="onPresetChange"
        >
          <option value="week">За неделю</option>
          <option value="month">За месяц</option>
          <option value="custom">Произвольный период</option>
        </select>
        <input
          v-if="periodPreset === 'custom'"
          v-model="dateFrom"
          type="date"
          class="rounded-md border border-slate-300 px-2 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        />
        <input
          v-if="periodPreset === 'custom'"
          v-model="dateTo"
          type="date"
          class="rounded-md border border-slate-300 px-2 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        />
        <button
          type="button"
          class="inline-flex items-center rounded-md bg-primary-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-primary-700"
          @click="loadData"
        >
          Обновить
        </button>
      </div>
    </header>

    <section class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <KpiCard
        label="Доход за период"
        :value="analytics.kpi.revenue"
        suffix="₽"
      />
      <KpiCard
        label="Расходы за период"
        :value="analytics.kpi.costs"
        suffix="₽"
      />
      <KpiCard
        label="Продано товаров"
        :value="analytics.kpi.soldCount"
      />
      <KpiCard
        label="Маржинальность"
        :value="analytics.kpi.margin"
        suffix="%"
      />
    </section>

    <section class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-slate-100 p-4">
        <h2 class="text-sm font-medium text-slate-800 mb-2">
          Динамика продаж / остатков
        </h2>
        <LineChart :points="analytics.salesTrend" />
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
        <h2 class="text-sm font-medium text-slate-800 mb-2">
          Структура продаж по категориям
        </h2>
        <DonutChart :items="analytics.salesByCategory" />
      </div>
    </section>

    <section class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-4 lg:col-span-2">
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-sm font-medium text-slate-800">Топ популярных товаров</h2>
          <button
            type="button"
            class="text-xs text-slate-600 hover:text-slate-900"
            @click="exportReport"
          >
            Экспорт в CSV
          </button>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full text-xs">
            <thead>
              <tr class="border-b border-slate-200 bg-slate-50 text-left text-[11px] uppercase tracking-wide text-slate-500">
                <th class="px-3 py-2">Товар</th>
                <th class="px-3 py-2">Категория</th>
                <th class="px-3 py-2">Продано</th>
                <th class="px-3 py-2">Доход</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in analytics.topProducts"
                :key="item.productId"
                class="border-b border-slate-100"
              >
                <td class="px-3 py-2 text-xs text-slate-800">
                  {{ item.name }}
                </td>
                <td class="px-3 py-2 text-xs text-slate-600">
                  {{ item.categoryName }}
                </td>
                <td class="px-3 py-2 text-xs text-slate-800">
                  {{ item.soldCount }}
                </td>
                <td class="px-3 py-2 text-xs text-slate-800">
                  {{ item.revenue.toLocaleString() }} ₽
                </td>
              </tr>
              <tr v-if="!loading && analytics.topProducts.length === 0">
                <td colspan="4" class="px-3 py-4 text-center text-xs text-slate-500">
                  Нет данных для выбранного периода.
                </td>
              </tr>
              <tr v-if="loading">
                <td colspan="4" class="px-3 py-4 text-center text-xs text-slate-500">
                  Загрузка данных...
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
        <h2 class="text-sm font-medium text-slate-800 mb-2">
          Табличный отчёт
        </h2>
        <p class="text-xs text-slate-500 mb-3">
          Детализированные показатели по дням. Для углублённого анализа используйте экспорт.
        </p>
        <button
          type="button"
          class="w-full inline-flex items-center justify-center rounded-md border border-slate-300 px-3 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50"
          @click="exportReport"
        >
          Экспорт в .xlsx / .csv
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import { statisticsService } from '@/services/statisticsService';
import KpiCard from '@/components/analytics/KpiCard.vue';
import LineChart from '@/components/analytics/LineChart.vue';
import DonutChart from '@/components/analytics/DonutChart.vue';

const loading = ref(false);

const periodPreset = ref('month');
const dateFrom = ref('');
const dateTo = ref('');

const analytics = reactive({
  kpi: {
    revenue: 0,
    costs: 0,
    soldCount: 0,
    margin: 0,
  },
  salesTrend: [],
  salesByCategory: [],
  topProducts: [],
});

function onPresetChange() {
  const today = new Date();
  if (periodPreset.value === 'week') {
    const from = new Date();
    from.setDate(today.getDate() - 7);
    dateFrom.value = from.toISOString().slice(0, 10);
    dateTo.value = today.toISOString().slice(0, 10);
  } else if (periodPreset.value === 'month') {
    const from = new Date();
    from.setMonth(today.getMonth() - 1);
    dateFrom.value = from.toISOString().slice(0, 10);
    dateTo.value = today.toISOString().slice(0, 10);
  }
}

async function loadData() {
  loading.value = true;
  try {
    const data = await statisticsService.getAnalytics({
      dateFrom: dateFrom.value,
      dateTo: dateTo.value,
    });
    Object.assign(analytics.kpi, data.kpi);
    analytics.salesTrend = data.salesTrend;
    analytics.salesByCategory = data.salesByCategory;
    analytics.topProducts = data.topProducts;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

async function exportReport() {
  try {
    await statisticsService.exportReport({
      dateFrom: dateFrom.value,
      dateTo: dateTo.value,
    });
  } catch (error) {
    console.error(error);
  }
}

onMounted(() => {
  onPresetChange();
  loadData();
});
</script>

