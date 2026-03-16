import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

const Login = () => import('@/views/auth/LoginView.vue');
const Register = () => import('@/views/auth/RegisterView.vue');
const Dashboard = () => import('@/views/DashboardView.vue');
const Products = () => import('@/views/catalog/ProductsView.vue');
const Categories = () => import('@/views/catalog/CategoriesView.vue');
const Suppliers = () => import('@/views/catalog/SuppliersView.vue');
const Upload = () => import('@/views/upload/UploadView.vue');
const Analytics = () => import('@/views/analytics/AnalyticsView.vue');
const Profile = () => import('@/views/profile/ProfileView.vue');
const Settings = () => import('@/views/profile/SettingsView.vue');

const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { public: true },
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
    meta: { public: true },
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'dashboard', component: Dashboard },
      { path: 'products', name: 'products', component: Products },
      { path: 'categories', name: 'categories', component: Categories },
      { path: 'suppliers', name: 'suppliers', component: Suppliers },
      { path: 'upload', name: 'upload', component: Upload },
      { path: 'analytics', name: 'analytics', component: Analytics },
      { path: 'profile', name: 'profile', component: Profile },
      { path: 'settings', name: 'settings', component: Settings },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (!to.meta.public && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } });
  } else if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
    next({ name: 'dashboard' });
  } else {
    next();
  }
});

export default router;

