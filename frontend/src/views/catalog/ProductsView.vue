<template>
  <div class="space-y-4">
    <header class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
      <div>
        <h1 class="text-xl font-semibold text-slate-900">Каталог товаров</h1>
        <p class="text-sm text-slate-500">
          Управление товарами, фильтрация, поиск и массовый импорт.
        </p>
      </div>
      <div class="flex gap-2">
        <button
          type="button"
          class="inline-flex items-center rounded-md border border-slate-300 bg-white px-3 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50"
          @click="showColumns = !showColumns"
        >
          Настроить колонки
        </button>
        <button
          type="button"
          class="inline-flex items-center rounded-md bg-primary-600 px-3 py-2 text-xs font-medium text-white hover:bg-primary-700"
          @click="openCreateModal"
        >
          Добавить товар
        </button>
      </div>
    </header>

    <section class="bg-white rounded-xl shadow-sm border border-slate-100 p-4 space-y-3">
      <div class="flex flex-col lg:flex-row gap-3">
        <div class="flex-1">
          <label class="block text-xs font-medium text-slate-600 mb-1">Поиск</label>
          <input
            v-model="filters.search"
            type="text"
            placeholder="Название или артикул"
            class="w-full rounded-md border border-slate-300 px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        <div class="flex-1">
          <label class="block text-xs font-medium text-slate-600 mb-1">Категория</label>
          <select
            v-model="filters.categoryId"
            class="w-full rounded-md border border-slate-300 px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          >
            <option value="">Все категории</option>
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>
        <div class="flex-1">
          <label class="block text-xs font-medium text-slate-600 mb-1">Поставщик</label>
          <select
            v-model="filters.supplierId"
            class="w-full rounded-md border border-slate-300 px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          >
            <option value="">Все поставщики</option>
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

      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <div>
          <label class="block text-xs font-medium text-slate-600 mb-1">Цена от</label>
          <input
            v-model.number="filters.priceFrom"
            type="number"
            class="w-full rounded-md border border-slate-300 px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-600 mb-1">Цена до</label>
          <input
            v-model.number="filters.priceTo"
            type="number"
            class="w-full rounded-md border border-slate-300 px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-600 mb-1">Остаток от</label>
          <input
            v-model.number="filters.stockFrom"
            type="number"
            class="w-full rounded-md border border-slate-300 px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-600 mb-1">Остаток до</label>
          <input
            v-model.number="filters.stockTo"
            type="number"
            class="w-full rounded-md border border-slate-300 px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
      </div>

      <div class="flex justify-end gap-2 text-xs">
        <button
          type="button"
          class="px-3 py-1.5 rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
          @click="resetFilters"
        >
          Сбросить
        </button>
        <button
          type="button"
          class="px-3 py-1.5 rounded-md bg-primary-600 text-white hover:bg-primary-700"
          @click="applyFilters"
        >
          Применить
        </button>
      </div>
    </section>

    <section class="bg-white rounded-xl shadow-sm border border-slate-100">
      <div class="overflow-x-auto">
        <table class="min-w-full text-xs">
          <thead>
            <tr class="border-b border-slate-200 bg-slate-50 text-left text-[11px] uppercase tracking-wide text-slate-500">
              <th v-if="visibleColumns.sku" class="px-3 py-2">Артикул</th>
              <th v-if="visibleColumns.name" class="px-3 py-2">Название</th>
              <th v-if="visibleColumns.category" class="px-3 py-2">Категория</th>
              <th v-if="visibleColumns.price" class="px-3 py-2">Цена</th>
              <th v-if="visibleColumns.stock" class="px-3 py-2">Остаток</th>
              <th v-if="visibleColumns.supplier" class="px-3 py-2">Поставщик</th>
              <th class="px-3 py-2 text-right">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="product in products"
              :key="product.id"
              class="border-b border-slate-100 hover:bg-slate-50"
            >
              <td v-if="visibleColumns.sku" class="px-3 py-2 font-mono text-[11px]">
                {{ product.sku }}
              </td>
              <td v-if="visibleColumns.name" class="px-3 py-2 text-xs text-slate-800">
                {{ product.name }}
              </td>
              <td v-if="visibleColumns.category" class="px-3 py-2 text-xs text-slate-600">
                {{ product.categoryName || '—' }}
              </td>
              <td v-if="visibleColumns.price" class="px-3 py-2 text-xs text-slate-800">
                {{ product.price.toLocaleString() }} {{ currency }}
              </td>
              <td v-if="visibleColumns.stock" class="px-3 py-2 text-xs text-slate-800">
                {{ product.stock }}
              </td>
              <td v-if="visibleColumns.supplier" class="px-3 py-2 text-xs text-slate-600">
                {{ product.supplierName || '—' }}
              </td>
              <td class="px-3 py-2 text-right">
                <button
                  type="button"
                  class="text-xs text-primary-600 hover:text-primary-700 mr-2"
                  @click="openEditModal(product)"
                >
                  Редактировать
                </button>
                <button
                  type="button"
                  class="text-xs text-red-600 hover:text-red-700"
                  @click="confirmDelete(product)"
                >
                  Удалить
                </button>
              </td>
            </tr>
            <tr v-if="!loading && products.length === 0">
              <td colspan="7" class="px-3 py-4 text-center text-xs text-slate-500">
                Товары не найдены. Попробуйте изменить фильтры или загрузить новые данные.
              </td>
            </tr>
            <tr v-if="loading">
              <td colspan="7" class="px-3 py-4 text-center text-xs text-slate-500">
                Загрузка данных...
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="flex items-center justify-between px-4 py-3 border-t border-slate-100 text-xs text-slate-600">
        <span>
          Страница {{ pagination.page }} из {{ totalPages }} (всего {{ pagination.total }} товаров)
        </span>
        <div class="flex items-center gap-2">
          <button
            type="button"
            class="px-2 py-1 rounded border border-slate-300 disabled:opacity-50"
            :disabled="pagination.page === 1"
            @click="changePage(pagination.page - 1)"
          >
            Назад
          </button>
          <button
            type="button"
            class="px-2 py-1 rounded border border-slate-300 disabled:opacity-50"
            :disabled="pagination.page === totalPages"
            @click="changePage(pagination.page + 1)"
          >
            Вперёд
          </button>
        </div>
      </div>
    </section>

    <ProductModal
      v-if="isProductModalOpen"
      :product="selectedProduct"
      :categories="categories"
      :suppliers="suppliers"
      :currency="currency"
      @close="closeProductModal"
      @saved="handleProductSaved"
    />

    <ColumnSettingsModal
      v-if="showColumns"
      :model-value="visibleColumns"
      @close="showColumns = false"
      @update:model-value="updateColumns"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { productService } from '@/services/productService';
import { categoryService } from '@/services/categoryService';
import { supplierService } from '@/services/supplierService';
import ProductModal from '@/components/catalog/ProductModal.vue';
import ColumnSettingsModal from '@/components/catalog/ColumnSettingsModal.vue';

const router = useRouter();
const route = useRoute();

const loading = ref(false);
const products = ref([]);
const categories = ref([]);
const suppliers = ref([]);

const currency = ref('₽');

const filters = reactive({
  search: route.query.search || '',
  categoryId: route.query.categoryId || '',
  supplierId: route.query.supplierId || '',
  priceFrom: route.query.priceFrom ? Number(route.query.priceFrom) : null,
  priceTo: route.query.priceTo ? Number(route.query.priceTo) : null,
  stockFrom: route.query.stockFrom ? Number(route.query.stockFrom) : null,
  stockTo: route.query.stockTo ? Number(route.query.stockTo) : null,
});

const pagination = reactive({
  page: route.query.page ? Number(route.query.page) : 1,
  pageSize: 20,
  total: 0,
});

const visibleColumns = reactive({
  sku: route.query.colSku !== '0',
  name: route.query.colName !== '0',
  category: route.query.colCategory !== '0',
  price: route.query.colPrice !== '0',
  stock: route.query.colStock !== '0',
  supplier: route.query.colSupplier !== '0',
});

const isProductModalOpen = ref(false);
const selectedProduct = ref(null);
const showColumns = ref(false);

const totalPages = computed(() =>
  pagination.total ? Math.ceil(pagination.total / pagination.pageSize) : 1,
);

function updateUrlQuery() {
  const query = {
    ...route.query,
    search: filters.search || undefined,
    categoryId: filters.categoryId || undefined,
    supplierId: filters.supplierId || undefined,
    priceFrom: filters.priceFrom || undefined,
    priceTo: filters.priceTo || undefined,
    stockFrom: filters.stockFrom || undefined,
    stockTo: filters.stockTo || undefined,
    page: pagination.page !== 1 ? pagination.page : undefined,
    colSku: visibleColumns.sku ? undefined : '0',
    colName: visibleColumns.name ? undefined : '0',
    colCategory: visibleColumns.category ? undefined : '0',
    colPrice: visibleColumns.price ? undefined : '0',
    colStock: visibleColumns.stock ? undefined : '0',
    colSupplier: visibleColumns.supplier ? undefined : '0',
  };

  router.replace({ query });
}

async function loadData() {
  loading.value = true;
  try {
    const [productsResult, categoriesResult, suppliersResult] = await Promise.all([
      productService.getList({
        page: pagination.page,
        pageSize: pagination.pageSize,
        ...filters,
      }),
      categoryService.getFlatList(),
      supplierService.getList(),
    ]);

    products.value = productsResult.items;
    pagination.total = productsResult.total;
    categories.value = categoriesResult;
    suppliers.value = suppliersResult.items;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

function resetFilters() {
  filters.search = '';
  filters.categoryId = '';
  filters.supplierId = '';
  filters.priceFrom = null;
  filters.priceTo = null;
  filters.stockFrom = null;
  filters.stockTo = null;
  pagination.page = 1;
  updateUrlQuery();
  loadData();
}

function applyFilters() {
  pagination.page = 1;
  updateUrlQuery();
  loadData();
}

function changePage(page) {
  pagination.page = page;
  updateUrlQuery();
  loadData();
}

function openCreateModal() {
  selectedProduct.value = null;
  isProductModalOpen.value = true;
}

function openEditModal(product) {
  selectedProduct.value = { ...product };
  isProductModalOpen.value = true;
}

function closeProductModal() {
  isProductModalOpen.value = false;
}

async function handleProductSaved() {
  isProductModalOpen.value = false;
  await loadData();
}

async function confirmDelete(product) {
  const confirmed = window.confirm(
    `Удалить товар "${product.name}" (артикул: ${product.sku})?`,
  );
  if (!confirmed) return;

  try {
    await productService.remove(product.id);
    await loadData();
  } catch (error) {
    console.error(error);
  }
}

function updateColumns(newValue) {
  Object.assign(visibleColumns, newValue);
  updateUrlQuery();
}

watch(
  () => route.query,
  (newQuery) => {
    if (newQuery.page && Number(newQuery.page) !== pagination.page) {
      pagination.page = Number(newQuery.page);
      loadData();
    }
  },
);

onMounted(loadData);
</script>

