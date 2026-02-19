import { createRouter, createWebHistory } from 'vue-router'
import ArticleDetail from '../views/ArticleDetail.vue'
import UploadPractice from '../views/UploadPractice.vue'
import FileDetail from '../views/FileDetail.vue'
import HotspotList from '../views/HotspotList.vue'
import HotspotDetail from '../views/HotspotDetail.vue'
import Favorites from '../views/Favorites.vue'
import ReadLater from '../views/ReadLater.vue'
import Settings from '../views/Settings.vue'

const routes = [
    { path: '/', component: () => import('../views/Home.vue') },
    { path: '/login', component: () => import('../views/Login.vue'), meta: { hideSidebar: true } },
    { path: '/register', component: () => import('../views/Register.vue'), meta: { hideSidebar: true } },
    { path: '/articles', component: () => import('../views/ArticleList.vue') },
    { path: '/articles/:id', component: ArticleDetail },
    { path: '/upload', component: UploadPractice },
    { path: '/upload/:id', component: FileDetail },
    { path: '/hotspots', component: HotspotList },
    { path: '/hotspots/:id', component: HotspotDetail },
    { path: '/favorites', component: Favorites },
    { path: '/read-later', component: ReadLater },
    { path: '/settings', component: Settings },
]

export default createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior: () => ({ top: 0 }),
})
