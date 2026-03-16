<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-100">
    <div class="w-full max-w-md bg-white shadow-lg rounded-xl p-8">
      <h1 class="text-2xl font-semibold text-slate-900 mb-2">Вход в систему</h1>
      <p class="text-sm text-slate-500 mb-6">
        Введите логин или email и пароль, чтобы продолжить.
      </p>

      <form class="space-y-4" @submit.prevent="onSubmit">
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Логин или Email</label>
          <input
            v-model.trim="form.login"
            type="text"
            class="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            :class="{ 'border-red-500': errors.login }"
            placeholder="user@example.com"
          />
          <p v-if="errors.login" class="mt-1 text-xs text-red-600">
            {{ errors.login }}
          </p>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Пароль</label>
          <input
            v-model="form.password"
            type="password"
            class="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            :class="{ 'border-red-500': errors.password }"
            placeholder="••••••••"
          />
          <p v-if="errors.password" class="mt-1 text-xs text-red-600">
            {{ errors.password }}
          </p>
        </div>

        <p v-if="apiError" class="text-sm text-red-600">
          {{ apiError }}
        </p>

        <button
          type="submit"
          class="w-full flex justify-center items-center rounded-md bg-primary-600 text-white text-sm font-medium px-4 py-2 hover:bg-primary-700 disabled:opacity-60"
          :disabled="submitting"
        >
          <span v-if="!submitting">Войти</span>
          <span v-else>Вход...</span>
        </button>
      </form>

      <p class="mt-4 text-xs text-slate-500">
        Нет аккаунта?
        <RouterLink to="/register" class="text-primary-600 hover:text-primary-700">
          Зарегистрироваться
        </RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { authService } from '@/services/authService';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const form = reactive({
  login: '',
  password: '',
});

const errors = reactive({
  login: '',
  password: '',
});

const submitting = ref(false);
const apiError = ref('');

function validate() {
  errors.login = '';
  errors.password = '';
  let valid = true;

  if (!form.login) {
    errors.login = 'Введите логин или email.';
    valid = false;
  }
  if (!form.password) {
    errors.password = 'Введите пароль.';
    valid = false;
  } else if (form.password.length < 6) {
    errors.password = 'Пароль должен быть не менее 6 символов.';
    valid = false;
  }

  return valid;
}

async function onSubmit() {
  apiError.value = '';
  if (!validate()) return;

  submitting.value = true;
  try {
    const { token, user } = await authService.login({
      login: form.login,
      password: form.password,
    });
    authStore.setAuth({ accessToken: token, userInfo: user });

    const redirect = route.query.redirect || '/';
    router.push(redirect);
  } catch (error) {
    apiError.value =
      error?.response?.data?.message ||
      'Неверный логин или пароль. Попробуйте ещё раз.';
  } finally {
    submitting.value = false;
  }
}
</script>

