<template>
  <div class="space-y-4 max-w-3xl">
    <header>
      <h1 class="text-xl font-semibold text-slate-900">Настройки системы</h1>
      <p class="text-sm text-slate-500">
        Управляйте настройками импорта, валютой и шаблонами маппинга.
      </p>
    </header>

    <section class="bg-white rounded-xl shadow-sm border border-slate-100 p-4 space-y-4">
      <h2 class="text-sm font-medium text-slate-800">Импорт по умолчанию</h2>
      <form class="space-y-3" @submit.prevent="saveImportSettings">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div>
            <label class="block text-xs font-medium text-slate-700 mb-1">Формат даты</label>
            <select
              v-model="importSettings.dateFormat"
              class="w-full rounded-md border border-slate-300 px-2 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="dd.MM.yyyy">dd.MM.yyyy</option>
              <option value="MM/dd/yyyy">MM/dd/yyyy</option>
              <option value="yyyy-MM-dd">yyyy-MM-dd</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-medium text-slate-700 mb-1">Разделитель CSV</label>
            <select
              v-model="importSettings.csvDelimiter"
              class="w-full rounded-md border border-slate-300 px-2 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value=",">Запятая (,)</option>
              <option value=";">Точка с запятой (;)</option>
              <option value="tab">Табуляция</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-medium text-slate-700 mb-1">Валюта</label>
            <select
              v-model="importSettings.currency"
              class="w-full rounded-md border border-slate-300 px-2 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="RUB">Рубли (RUB)</option>
              <option value="USD">Доллары (USD)</option>
              <option value="EUR">Евро (EUR)</option>
            </select>
          </div>
        </div>

        <div class="flex justify-end">
          <button
            type="submit"
            class="inline-flex items-center rounded-md bg-primary-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-primary-700"
          >
            Сохранить настройки
          </button>
        </div>
      </form>
    </section>

    <section class="bg-white rounded-xl shadow-sm border border-slate-100 p-4 space-y-3">
      <div class="flex items-center justify-between">
        <h2 class="text-sm font-medium text-slate-800">Шаблоны маппинга полей</h2>
        <button
          type="button"
          class="inline-flex items-center rounded-md border border-slate-300 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50"
          @click="reloadTemplates"
        >
          Обновить список
        </button>
      </div>

      <div v-if="mappingTemplates.length === 0" class="text-xs text-slate-500">
        Шаблоны маппинга ещё не созданы. Их можно сохранить на странице загрузки данных.
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full text-xs">
          <thead>
            <tr class="border-b border-slate-200 bg-slate-50 text-left text-[11px] uppercase tracking-wide text-slate-500">
              <th class="px-3 py-2">Название</th>
              <th class="px-3 py-2">Дата создания</th>
              <th class="px-3 py-2 text-right">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="tpl in mappingTemplates"
              :key="tpl.id"
              class="border-b border-slate-100"
            >
              <td class="px-3 py-2 text-xs text-slate-800">
                {{ tpl.name }}
              </td>
              <td class="px-3 py-2 text-xs text-slate-500">
                {{ tpl.createdAt }}
              </td>
              <td class="px-3 py-2 text-right">
                <button
                  type="button"
                  class="text-xs text-red-600 hover:text-red-700"
                  @click="removeTemplate(tpl)"
                >
                  Удалить
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import { settingsService } from '@/services/settingsService';
import { mappingTemplateService } from '@/services/mappingTemplateService';

const importSettings = reactive({
  dateFormat: 'dd.MM.yyyy',
  csvDelimiter: ';',
  currency: 'RUB',
});

const mappingTemplates = ref([]);

async function loadImportSettings() {
  try {
    const data = await settingsService.getImportSettings();
    Object.assign(importSettings, data);
  } catch (error) {
    console.error(error);
  }
}

async function saveImportSettings() {
  try {
    await settingsService.updateImportSettings({ ...importSettings });
  } catch (error) {
    console.error(error);
  }
}

async function reloadTemplates() {
  try {
    mappingTemplates.value = await mappingTemplateService.getList();
  } catch (error) {
    console.error(error);
  }
}

async function removeTemplate(tpl) {
  const confirmed = window.confirm(`Удалить шаблон "${tpl.name}"?`);
  if (!confirmed) return;
  try {
    await mappingTemplateService.remove(tpl.id);
    await reloadTemplates();
  } catch (error) {
    console.error(error);
  }
}

onMounted(async () => {
  await Promise.all([loadImportSettings(), reloadTemplates()]);
});
</script>

