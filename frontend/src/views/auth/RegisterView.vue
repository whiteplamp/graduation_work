<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-100">
    <div class="w-full max-w-md bg-white shadow-lg rounded-xl p-8">
      <h1 class="text-2xl font-semibold text-slate-900 mb-2">Регистрация</h1>
      <p class="text-sm text-slate-500 mb-6">
        Создайте новый аккаунт для работы с каталогом.
      </p>

      <form class="space-y-4" @submit.prevent="onSubmit">
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Имя</label>
          <input
            v-model.trim="form.name"
            type="text"
            class="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            :class="{ 'border-red-500': errors.name }"
            placeholder="Иван Иванов"
          />
          <p v-if="errors.name" class="mt-1 text-xs text-red-600">
            {{ errors.name }}
          </p>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
          <input
            v-model.trim="form.email"
            type="email"
            class="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            :class="{ 'border-red-500': errors.email }"
            placeholder="user@example.com"
          />
          <p v-if="errors.email" class="mt-1 text-xs text-red-600">
            {{ errors.email }}
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

        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Повторите пароль</label>
          <input
            v-model="form.passwordConfirmation"
            type="password"
            class="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            :class="{ 'border-red-500': errors.passwordConfirmation }"
            placeholder="••••••••"
          />
          <p v-if="errors.passwordConfirmation" class="mt-1 text-xs text-red-600">
            {{ errors.passwordConfirmation }}
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
          <span v-if="!submitting">Зарегистрироваться</span>
          <span v-else>Создание аккаунта...</span>
        </button>
      </form>

      <p class="mt-4 text-xs text-slate-500">
        Уже есть аккаунт?
        <RouterLink to="/login" class="text-primary-600 hover:text-primary-700">
          Войти
        </RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter, RouterLink } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { authService } from '@/services/authService';

const router = useRouter();
const authStore = useAuthStore();

const form = reactive({
  name: '',
  email: '',
  password: '',
  passwordConfirmation: '',
});

const errors = reactive({
  name: '',
  email: '',
  password: '',
  passwordConfirmation: '',
});

const submitting = ref(false);
const apiError = ref('');

function validate() {
  errors.name = '';
  errors.email = '';
  errors.password = '';
  errors.passwordConfirmation = '';
  let valid = true;

  if (!form.name) {
    errors.name = 'Введите имя.';
    valid = false;
  }
  if (!form.email) {
    errors.email = 'Введите email.';
    valid = false;
  } else if (!/\S+@\S+\.\S+/.test(form.email)) {
    errors.email = 'Введите корректный email.';
    valid = false;
  }
  if (!form.password) {
    errors.password = 'Введите пароль.';
    valid = false;
  } else if (form.password.length < 6) {
    errors.password = 'Пароль должен быть не менее 6 символов.';
    valid = false;
  }
  if (form.passwordConfirmation !== form.password) {
    errors.passwordConfirmation = 'Пароли не совпадают.';
    valid = false;
  }

  return valid;
}

async function onSubmit() {
  apiError.value = '';
  if (!validate()) return;

  submitting.value = true;
  try {
    const { token, user } = await authService.register({
      name: form.name,
      email: form.email,
      password: form.password,
    });
    authStore.setAuth({ accessToken: token, userInfo: user });
    router.push('/');
  } catch (error) {
    apiError.value =
      error?.response?.data?.message ||
      'Не удалось зарегистрироваться. Попробуйте позже.';
  } finally {
    submitting.value = false;
  }
}
</script>

