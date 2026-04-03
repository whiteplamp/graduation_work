<template>
  <div class="space-y-4">
    <header>
      <h1 class="text-xl font-semibold text-slate-900">Загрузка данных</h1>
      <p class="text-sm text-slate-500">
        Загрузите .xlsx или .csv файл, сопоставьте поля и отслеживайте статус обработки.
      </p>
    </header>

    <section class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-slate-100 p-4 space-y-4">
        <h2 class="text-sm font-medium text-slate-800">Шаг 1. Загрузка файла</h2>

        <div
          class="border-2 border-dashed rounded-xl px-4 py-10 text-center"
          :class="dragActive ? 'border-primary-400 bg-primary-50' : 'border-slate-300 bg-slate-50'"
          @dragover.prevent="dragActive = true"
          @dragleave.prevent="dragActive = false"
          @drop.prevent="onDrop"
        >
          <p class="text-sm font-medium text-slate-800 mb-1">
            Перетащите файл сюда
          </p>
          <p class="text-xs text-slate-500 mb-3">
            Поддерживаются файлы .xlsx и .csv
          </p>
          <input
            ref="fileInput"
            type="file"
            class="hidden"
            accept=".xlsx,.xls,.csv"
            @change="onFileChange"
          />
          <button
            type="button"
            class="inline-flex items-center rounded-md bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm border border-slate-300 hover:bg-slate-50"
            @click="fileInput?.click()"
          >
            Выбрать файл
          </button>
          <p v-if="fileName" class="mt-3 text-xs text-slate-600">
            Выбран файл: <span class="font-medium">{{ fileName }}</span>
          </p>
        </div>

        <div class="space-y-2">
          <h3 class="text-sm font-medium text-slate-800">Тип загрузки</h3>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs">
            <label class="flex items-start gap-2 rounded-md border border-slate-300 px-3 py-2 cursor-pointer">
              <input
                v-model="mode"
                type="radio"
                value="replace"
                class="mt-0.5"
              />
              <span>
                <span class="block font-medium">Замена каталога</span>
                <span class="block text-slate-500">
                  Полная перезапись текущего каталога содержимым файла.
                </span>
              </span>
            </label>
            <label class="flex items-start gap-2 rounded-md border border-slate-300 px-3 py-2 cursor-pointer">
              <input
                v-model="mode"
                type="radio"
                value="append"
                class="mt-0.5"
              />
              <span>
                <span class="block font-medium">Добавление</span>
                <span class="block text-slate-500">
                  Добавление новых товаров к существующему каталогу.
                </span>
              </span>
            </label>
            <label class="flex items-start gap-2 rounded-md border border-slate-300 px-3 py-2 cursor-pointer">
              <input
                v-model="mode"
                type="radio"
                value="update"
                class="mt-0.5"
              />
              <span>
                <span class="block font-medium">Обновление по артикулу</span>
                <span class="block text-slate-500">
                  Обновление существующих товаров по артикулу, добавление новых.
                </span>
              </span>
            </label>
          </div>
        </div>

        <div class="flex justify-end">
          <button
            type="button"
            class="inline-flex items-center rounded-md bg-primary-600 px-3 py-2 text-xs font-medium text-white hover:bg-primary-700 disabled:opacity-50"
            :disabled="!file || uploading"
            @click="upload"
          >
            <span v-if="!uploading">Загрузить и показать предпросмотр</span>
            <span v-else>Загрузка...</span>
          </button>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-4 space-y-3">
        <h2 class="text-sm font-medium text-slate-800">Статус обработки</h2>
        <div v-if="!uploadJobId" class="text-xs text-slate-500">
          Загрузите файл, чтобы увидеть прогресс обработки.
        </div>
        <div v-else class="space-y-2 text-xs">
          <p>
            Текущий статус:
            <span class="font-medium">{{ statusLabel }}</span>
          </p>
          <div class="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
            <div
              class="h-2 bg-primary-500"
              :style="{ width: progress + '%' }"
            />
          </div>
          <p class="text-slate-500">
            Обработано {{ processedRows }} из {{ totalRows }} строк.
          </p>
          <button
            v-if="errorReportUrl"
            type="button"
            class="inline-flex items-center rounded-md border border-slate-300 px-3 py-1.5 text-[11px] font-medium text-slate-700 hover:bg-slate-50"
            @click="downloadErrorReport"
          >
            Скачать отчёт об ошибках
          </button>
        </div>
      </div>
    </section>

    <section v-if="previewColumns.length" class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-slate-100 p-4 space-y-3">
        <h2 class="text-sm font-medium text-slate-800">Шаг 1. Предпросмотр данных</h2>
        <p class="text-xs text-slate-500">
          Показаны первые {{ previewRows.length }} строк файла.
        </p>
        <div class="overflow-x-auto">
          <table class="min-w-full text-xs">
            <thead>
              <tr class="border-b border-slate-200 bg-slate-50 text-left text-[11px] uppercase tracking-wide text-slate-500">
                <th
                  v-for="col in previewColumns"
                  :key="col"
                  class="px-3 py-2"
                >
                  {{ col }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(row, index) in previewRows"
                :key="index"
                class="border-b border-slate-100"
              >
                <td
                  v-for="col in previewColumns"
                  :key="col"
                  class="px-3 py-1.5 text-xs text-slate-700"
                >
                  {{ row[col] }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-4 space-y-3">
        <h2 class="text-sm font-medium text-slate-800">Шаг 2. Маппинг полей</h2>
        <p class="text-xs text-slate-500">
          Сопоставьте колонки файла с полями системы.
        </p>
        <div class="space-y-2 text-xs">
          <div
            v-for="field in systemFields"
            :key="field.key"
            class="flex flex-col"
          >
            <label class="mb-1 font-medium">
              {{ field.label }}
              <span v-if="field.required" class="text-red-500">*</span>
            </label>
            <select
              v-model="mapping[field.key]"
              class="rounded-md border border-slate-300 px-2 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="">Не выбрано</option>
              <option
                v-for="col in previewColumns"
                :key="col"
                :value="col"
              >
                {{ col }}
              </option>
            </select>
          </div>
        </div>

        <div class="space-y-2">
          <label class="text-xs font-medium text-slate-700">
            Шаблон маппинга
          </label>
          <select
            v-model="selectedTemplateId"
            class="w-full rounded-md border border-slate-300 px-2 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            @change="applyTemplate"
          >
            <option value="">Не выбран</option>
            <option
              v-for="tpl in mappingTemplates"
              :key="tpl.id"
              :value="tpl.id"
            >
              {{ tpl.name }}
            </option>
          </select>
          <button
            type="button"
            class="inline-flex items-center rounded-md border border-slate-300 px-3 py-1.5 text-[11px] font-medium text-slate-700 hover:bg-slate-50"
            :disabled="!Object.values(mapping).some(Boolean)"
            @click="saveTemplate"
          >
            Сохранить как шаблон
          </button>
        </div>

        <button
          type="button"
          class="w-full inline-flex items-center justify-center rounded-md bg-primary-600 px-3 py-2 text-xs font-medium text-white hover:bg-primary-700 disabled:opacity-50"
          :disabled="!canStartProcessing || processing"
          @click="startProcessing"
        >
          <span v-if="!processing">Запустить обработку файла</span>
          <span v-else>Обработка запускается...</span>
        </button>
      </div>
    </section>

    <section class="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
      <h2 class="text-sm font-medium text-slate-800 mb-3">Последние загрузки</h2>
      <div v-if="recentJobs.length === 0" class="text-xs text-slate-500">
        История загрузок пока пуста.
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full text-xs">
          <thead>
            <tr class="border-b border-slate-200 bg-slate-50 text-left text-[11px] uppercase tracking-wide text-slate-500">
              <th class="px-3 py-2">Файл</th>
              <th class="px-3 py-2">Тип загрузки</th>
              <th class="px-3 py-2">Статус</th>
              <th class="px-3 py-2">Успешно</th>
              <th class="px-3 py-2">Ошибки</th>
              <th class="px-3 py-2">Дата</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="job in recentJobs"
              :key="job.id"
              class="border-b border-slate-100"
            >
              <td class="px-3 py-2 text-xs text-slate-800">
                {{ job.fileName }}
              </td>
              <td class="px-3 py-2 text-xs text-slate-600">
                {{ job.modeLabel }}
              </td>
              <td class="px-3 py-2">
                <span
                  class="inline-flex items-center rounded-full px-2 py-0.5 text-[11px] font-medium"
                  :class="statusPillClass(job.status)"
                >
                  {{ job.statusLabel }}
                </span>
              </td>
              <td class="px-3 py-2 text-xs text-slate-700">
                {{ job.successCount }}
              </td>
              <td class="px-3 py-2 text-xs text-red-600">
                {{ job.errorCount }}
              </td>
              <td class="px-3 py-2 text-xs text-slate-500">
                {{ job.createdAt }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue';
import { uploadService } from '@/services/uploadService';
import { mappingTemplateService } from '@/services/mappingTemplateService';

const fileInput = ref(null);
const dragActive = ref(false);
const file = ref(null);
const fileName = ref('');
const mode = ref('update');
const uploading = ref(false);
const processing = ref(false);

const uploadJobId = ref(null);
const progress = ref(0);
const processedRows = ref(0);
const totalRows = ref(0);
const status = ref('');
const errorReportUrl = ref('');

const previewColumns = ref([]);
const previewRows = ref([]);

const systemFields = [
  { key: 'sku', label: 'Артикул', required: true },
  { key: 'name', label: 'Название товара', required: true },
  { key: 'category', label: 'Категория', required: false },
  { key: 'price', label: 'Цена', required: false },
  { key: 'stock', label: 'Остаток', required: false },
  { key: 'supplier', label: 'Поставщик', required: false },
];

const mapping = reactive({
  sku: '',
  name: '',
  category: '',
  price: '',
  stock: '',
  supplier: '',
});

const mappingTemplates = ref([]);
const selectedTemplateId = ref('');

const recentJobs = ref([]);

const statusLabel = computed(() => {
  if (status.value === 'processing') return 'Идёт обработка';
  if (status.value === 'queued') return 'В очереди';
  if (status.value === 'completed') return 'Завершена';
  if (status.value === 'failed') return 'Ошибка';
  return '—';
});

const canStartProcessing = computed(() =>
  systemFields
    .filter((f) => f.required)
    .every((f) => !!mapping[f.key]),
);

function statusPillClass(val) {
  if (val === 'completed') return 'bg-green-100 text-green-700';
  if (val === 'processing' || val === 'queued') return 'bg-amber-100 text-amber-700';
  if (val === 'failed') return 'bg-red-100 text-red-700';
  return 'bg-slate-100 text-slate-600';
}

function onFileChange(event) {
  const selected = event.target.files?.[0];
  if (!selected) return;
  file.value = selected;
  fileName.value = selected.name;
}

function onDrop(event) {
  dragActive.value = false;
  const droppedFile = event.dataTransfer.files?.[0];
  if (!droppedFile) return;
  file.value = droppedFile;
  fileName.value = droppedFile.name;
}

async function upload() {
    if (!file.value) return

    uploading.value = true
    let uploadResult = null

    try {
        const result = await uploadService.uploadFile(file.value)
        uploadResult = result

        // Если есть ошибки, показываем их
        if (result.errors && result.errors.length) {
            console.warn('Ошибки при загрузке:', result.errors)
        }

    } catch (error) {
        console.error('Upload error:', error)
        uploadResult = {
            success: false,
            message: error.response?.data?.detail || 'Ошибка при загрузке файла',
            total_rows: 0,
            created: 0,
            updated: 0,
            errors: [error.response?.data?.detail || error.message]
        }
    } finally {
        uploading.value = false
    }
}

async function loadStatus() {
  if (!uploadJobId.value) return;
  try {
    const job = await uploadService.getStatus(uploadJobId.value);
    progress.value = job.progress;
    processedRows.value = job.processedRows;
    totalRows.value = job.totalRows;
    status.value = job.status;
    errorReportUrl.value = job.errorReportUrl || '';
  } catch (error) {
    console.error(error);
  }
}

async function startProcessing() {
  if (!uploadJobId.value) return;
  processing.value = true;
  try {
    await uploadService.startProcessing(uploadJobId.value, { mapping });
    await loadStatus();
  } catch (error) {
    console.error(error);
  } finally {
    processing.value = false;
  }
}

async function downloadErrorReport() {
  if (!uploadJobId.value) return;
  try {
    await uploadService.downloadErrorReport(uploadJobId.value);
  } catch (error) {
    console.error(error);
  }
}

async function loadTemplates() {
  mappingTemplates.value = await mappingTemplateService.getList();
}

async function loadRecentJobs() {
  recentJobs.value = await uploadService.getRecentJobs();
}

function applyTemplate() {
  const tpl = mappingTemplates.value.find((t) => t.id === selectedTemplateId.value);
  if (!tpl) return;
  Object.assign(mapping, tpl.mapping);
}

async function saveTemplate() {
  const name = window.prompt('Введите название шаблона маппинга');
  if (!name) return;
  try {
    await mappingTemplateService.create({
      name,
      mapping: { ...mapping },
    });
    await loadTemplates();
  } catch (error) {
    console.error(error);
  }
}

onMounted(async () => {
  await Promise.all([loadTemplates(), loadRecentJobs()]);
});
</script>

