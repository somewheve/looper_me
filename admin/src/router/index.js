import Vue from 'vue'
import Router from 'vue-router'
/* Layout */
import Layout from '@/layout'

Vue.use(Router)

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [{
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: '控制台',
      component: () => import('@/views/dashboard/index'),
      meta: {
        title: 'looper_me',
        icon: 'bee'
      }
    }]
  },
  {
    path: '/data_manager',
    component: Layout,
    redirect: '/',
    name: 'data_manager',
    meta: {
      title: '数据管理',
      icon: 'example'
    },
    children: [{
        path: 'table',
        name: 'Table',
        component: () => import('@/views/table/index'),
        meta: {
          title: '数据下载',
          icon: 'table'
        }
      },
      {
        path: 'tree',
        name: 'Tree',
        component: () => import('@/views/tree/index'),
        meta: {
          title: '数据查找',
          icon: 'tree'
        }
      }
    ]
  },
  {
    path: '/download',
    component: Layout,
    redirect:'/data_manager/table',
    meta: {
      title: '数据下载',
      icon: 'table'
    },
    children: [{
      path: 'index',
      name: 'download',
      component: () => import('@/views/download/index'),
      meta: {
        title: '下载'
      }
    }],
    hidden: true
  },
  {
    path: '/ip_manage',
    component: Layout,
    children: [{
      path: 'index',
      name: 'ip_manage',
      component: () => import('@/views/form/index'),
      meta: {
        title: 'IP管理',
        icon: 'form'
      }
    }]
  },
  {
    path: '/black_house',
    component: Layout,
    children: [{
      path: 'index',
      name: 'black_house',
      component: () => import('@/views/blackHouse/index'),
      meta: {
        title: '小黑屋',
        icon: 'house'
      }
    }]
  },
  {
    path: '/server',
    component: Layout,
    children: [{
      path: 'index',
      name: 'server',
      component: () => import('@/views/server/index'),
      meta: {
        title: '源服务器管理',
        icon: 'server'
      }
    }]
  },

  {
    path: '/config',
    component: Layout,
    redirect: '/',
    name: 'Nested',
    meta: {
      title: '服务器配置项',
      icon: 'configure'
    },
    children: [{
        path: 'base',
        component: () => import('@/views/nested/menu1/index'), // Parent router-view
        name: 'base',
        meta: {
          title: '基础配置',
          icon:'configuration'
        }
      },
      {
        path: 'high_level',
        component: () => import('@/views/nested/menu2/index'),
        meta: {
          title: '高级配置',
          icon:'configuration_1'
        }
      }
    ]
  },

  // 404 page must be placed at the end !!!
  {
    path: '*',
    redirect: '/404',
    hidden: true
  }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({
    y: 0
  }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}
export default router
