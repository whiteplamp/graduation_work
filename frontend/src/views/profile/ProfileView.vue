<template>
  <div class="space-y-4 max-w-2xl">
    <header>
      <h1 class="text-xl font-semibold text-slate-900">Профиль пользователя</h1>
      <p class="text-sm text-slate-500">
        Обновите личные данные и пароль.
      </p>
    </header>

    <section class="bg-white rounded-xl shadow-sm border border-slate-100 p-4 space-y-4">
      <h2 class="text-sm font-medium text-slate-800">Личные данные</h2>
      <form class="space-y-3" @submit.prevent="saveProfile">
        <div>
          <label class="block text-xs font-medium text-slate-700 mb-1">Имя</label>
          <input
            v-model="profile.name"
            type="text"
            class="w-full rounded-md border border-slate-300 px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-700 mb-1">Email</label>
          <input
            v-model="profile.email"
            type="email"
            class="w-full rounded-md border border-slate-300 px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        <div class="flex justify-end">
          <button
            type="submit"
            class="inline-flex items-center rounded-md bg-primary-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-primary-700"
          >
            Сохранить
          </button>
        </div>
      </form>
    </section>

    <section class="bg-white rounded-xl shadow-sm border border-slate-100 p-4 space-y-4">
      <h2 class="text-sm font-medium text-slate-800">Смена пароля</h2>
      <form class="space-y-3" @submit.prevent="changePassword">
        <div>
          <label class="block text-xs font-medium text-slate-700 mb-1">Текущий пароль</label>
          <input
            v-model="passwordForm.currentPassword"
            type="password"
            class="w-full rounded-md border border-slate-300 px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-700 mb-1">Новый пароль</label>
          <input
            v-model="passwordForm.newPassword"
            type="password"
            class="w-full rounded-md border border-slate-300 px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-700 mb-1">Повторите новый пароль</label>
          <input
            v-model="passwordForm.newPasswordConfirmation"
            type="password"
            class="w-full rounded-md border border-slate-300 px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        <div class="flex justify-end">
          <button
            type="submit"
            class="inline-flex items-center rounded-md border border-slate-300 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50"
          >
            Обновить пароль
          </button>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup>
import { onMounted, reactive } from 'vue';
import { profileService } from '@/services/profileService';
import { useAuthStore } from '@/stores/authStore';

const authStore = useAuthStore();

const profile = reactive({
  name: '',
  email: '',
});

const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  newPasswordConfirmation: '',
});

onMounted(async () => {
  try {
    const data = await profileService.getProfile();
    profile.name = data.name;
    profile.email = data.email;
  } catch (error) {
    console.error(error);
  }
});

async function saveProfile() {
  try {
    const updated = await profileService.updateProfile({
      name: profile.name,
      email: profile.email,
    });
    authStore.user = updated;
  } catch (error) {
    console.error(error);
  }
}

async function changePassword() {
  try {
    await profileService.changePassword({ ...passwordForm });
    passwordForm.currentPassword = '';
    passwordForm.newPassword = '';
    passwordForm.newPasswordConfirmation = '';
  } catch (error) {
    console.error(error);
  }
}
</script>

