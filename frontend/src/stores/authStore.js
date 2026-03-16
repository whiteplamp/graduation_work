import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

const TOKEN_KEY = 'auth_token';

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem(TOKEN_KEY) || '');
  const user = ref(null);

  const isAuthenticated = computed(() => !!token.value);

  function setAuth({ accessToken, userInfo }) {
    token.value = accessToken;
    user.value = userInfo || null;
    localStorage.setItem(TOKEN_KEY, accessToken);
  }

  function clearAuth() {
    token.value = '';
    user.value = null;
    localStorage.removeItem(TOKEN_KEY);
  }

  return {
    token,
    user,
    isAuthenticated,
    setAuth,
    clearAuth,
  };
});

