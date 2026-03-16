<template>
  <div class="space-y-4">
    <header class="flex items-center justify-between">
      <div>
        <h1 class="text-xl font-semibold text-slate-900">Категории</h1>
        <p class="text-sm text-slate-500">
          Управляйте древовидной структурой категорий товаров.
        </p>
      </div>
      <button
        type="button"
        class="inline-flex items-center rounded-md bg-primary-600 px-3 py-2 text-xs font-medium text-white hover:bg-primary-700"
        @click="openCreateRoot"
      >
        Добавить категорию
      </button>
    </header>

    <section class="bg-white rounded-xl shadow-sm border border-slate-100 p-4">
      <div v-if="loading" class="text-xs text-slate-500">
        Загрузка категорий...
      </div>
      <div v-else-if="tree.length === 0" class="text-xs text-slate-500">
        Категорий пока нет. Создайте первую категорию.
      </div>
      <ul v-else class="space-y-1 text-sm">
        <CategoryNode
          v-for="node in tree"
          :key="node.id"
          :node="node"
          @create-child="openCreateChild"
          @edit="openEdit"
          @remove="confirmDelete"
        />
      </ul>
    </section>

    <CategoryModal
      v-if="modalOpen"
      :category="selectedCategory"
      :parent="parentCategory"
      @close="modalOpen = false"
      @saved="handleSaved"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { categoryService } from '@/services/categoryService';
import CategoryNode from '@/components/catalog/CategoryNode.vue';
import CategoryModal from '@/components/catalog/CategoryModal.vue';

const loading = ref(false);
const tree = ref([]);

const modalOpen = ref(false);
const selectedCategory = ref(null);
const parentCategory = ref(null);

async function loadTree() {
  loading.value = true;
  try {
    tree.value = await categoryService.getTree();
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

function openCreateRoot() {
  selectedCategory.value = null;
  parentCategory.value = null;
  modalOpen.value = true;
}

function openCreateChild(parent) {
  selectedCategory.value = null;
  parentCategory.value = parent;
  modalOpen.value = true;
}

function openEdit(category) {
  selectedCategory.value = { ...category };
  parentCategory.value = null;
  modalOpen.value = true;
}

async function confirmDelete(category) {
  const confirmed = window.confirm(
    `Удалить категорию "${category.name}" и все подкатегории?`,
  );
  if (!confirmed) return;

  try {
    await categoryService.remove(category.id);
    await loadTree();
  } catch (error) {
    console.error(error);
  }
}

async function handleSaved() {
  modalOpen.value = false;
  await loadTree();
}

onMounted(loadTree);
</script>

