<template>
  <li>
    <div class="flex items-center justify-between rounded-md px-2 py-1 hover:bg-slate-50">
      <div class="flex items-center gap-1">
        <button
          v-if="hasChildren"
          type="button"
          class="w-5 h-5 flex items-center justify-center text-slate-500 hover:text-slate-700"
          @click="expanded = !expanded"
        >
          {{ expanded ? '−' : '+' }}
        </button>
        <span v-else class="w-5" />
        <span class="text-xs text-slate-800">
          {{ node.name }}
        </span>
      </div>
      <div class="flex items-center gap-1 text-[11px]">
        <button
          type="button"
          class="px-2 py-0.5 rounded border border-slate-300 text-slate-600 hover:bg-slate-50"
          @click="$emit('create-child', node)"
        >
          Подкатегория
        </button>
        <button
          type="button"
          class="px-2 py-0.5 rounded border border-slate-300 text-slate-600 hover:bg-slate-50"
          @click="$emit('edit', node)"
        >
          Редактировать
        </button>
        <button
          type="button"
          class="px-2 py-0.5 rounded border border-red-200 text-red-600 hover:bg-red-50"
          @click="$emit('remove', node)"
        >
          Удалить
        </button>
      </div>
    </div>

    <ul
      v-if="hasChildren && expanded"
      class="mt-1 ml-4 border-l border-slate-100 pl-3 space-y-1"
    >
      <CategoryNode
        v-for="child in node.children"
        :key="child.id"
        :node="child"
        @create-child="$emit('create-child', $event)"
        @edit="$emit('edit', $event)"
        @remove="$emit('remove', $event)"
      />
    </ul>
  </li>
</template>

<script setup>
import { computed, ref } from 'vue';

const props = defineProps({
  node: {
    type: Object,
    required: true,
  },
});

const expanded = ref(true);

const hasChildren = computed(
  () => Array.isArray(props.node.children) && props.node.children.length > 0,
);
</script>

