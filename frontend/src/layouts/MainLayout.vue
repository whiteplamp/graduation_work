<template>
  <div class="min-h-screen flex bg-slate-100">
    <aside class="w-64 bg-slate-900 text-slate-100 flex flex-col">
      <div class="h-16 flex items-center px-6 border-b border-slate-800">
        <span class="font-semibold text-lg">Каталог товаров</span>
      </div>
      <nav class="flex-1 overflow-y-auto px-3 py-4 space-y-1 text-sm">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="flex items-center px-3 py-2 rounded-md hover:bg-slate-800"
          :class="{
            'bg-slate-800 text-white': route.name === item.name,
            'text-slate-300': route.name !== item.name,
          }"
        >
          <span class="mr-2">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>
      <div class="border-t border-slate-800 px-4 py-3 text-xs text-slate-400">
        <button class="w-full text-left hover:text-slate-200" @click="onLogout">
          Выйти
        </button>
      </div>
    </aside>

    <div class="flex-1 flex flex-col">
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
        <div class="font-medium text-slate-800">
          {{ currentTitle }}
        </div>
        <div class="flex items-center gap-3 text-sm text-slate-600">
          <RouterLink
            to="/profile"
            class="hover:text-slate-900"
          >
            {{ authStore.user?.name || 'Профиль' }}
          </RouterLink>
        </div>
      </header>

      <main class="flex-1 p-6 overflow-y-auto">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter, RouterLink, RouterView } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const navItems = [
  { name: 'dashboard', to: '/', label: 'Дашборд', icon: '🏠' },
  { name: 'products', to: '/products', label: 'Каталог товаров', icon: '📦' },
  { name: 'categories', to: '/categories', label: 'Категории', icon: '📂' },
  { name: 'suppliers', to: '/suppliers', label: 'Поставщики', icon: '🏭' },
  { name: 'upload', to: '/upload', label: 'Загрузка данных', icon: '⬆️' },
  { name: 'analytics', to: '/analytics', label: 'Аналитика', icon: '📊' },
  { name: 'settings', to: '/settings', label: 'Настройки', icon: '⚙️' },
];

const currentTitle = computed(() => {
  const current = navItems.find((item) => item.name === route.name);
  return current ? current.label : 'Панель управления';
});

function onLogout() {
  authStore.clearAuth();
  router.push({ name: 'login' });
}
</script>

