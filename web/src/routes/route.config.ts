import NotFound from '@/pages/NotFound';
import Books from '@/pages/Books';
import Home from '@/pages/Home';
import Members from '@/pages/Members';
import Rule from '@/pages/Rule';
import {
  HomeOutlined,
  UserOutlined,
  BookOutlined,
  TagsOutlined,
  FormOutlined,
  ApartmentOutlined,
} from '@ant-design/icons';
import LoanSlips from '@/pages/LoanSlips';
import LoginPage from '@/pages/Login';
import RegisterPage from '@/pages/Register';
import Organization from '@/pages/Organization';

export interface IRoute {
  path: string;
  title: string;
  name: string;
  icon: any;
  showInMenu: boolean;
  component: React.ComponentType<any>;
}

export const authRouter: any = [
  {
    path: 'login',
    name: 'Đăng nhập',
    title: 'Login',
    component: LoginPage,
    showInMenu: false,
  },
  {
    path: 'register',
    name: 'Đăng ký',
    title: 'Register',
    component: RegisterPage,
    showInMenu: false,
  },
];

export const appRouters: IRoute[] = [
  {
    path: '/',
    title: 'home',
    name: 'Trang chủ',
    icon: HomeOutlined,
    showInMenu: true,
    component: Home,
  },
  {
    path: '/books',
    title: 'books',
    name: 'Sách',
    icon: BookOutlined,
    showInMenu: true,
    component: Books,
  },
  {
    path: '/loanslips',
    title: 'loanslips',
    name: 'Phiếu mượn',
    icon: FormOutlined,
    showInMenu: true,
    component: LoanSlips,
  },
  {
    path: '/members',
    title: 'members',
    name: 'Thành viên',
    icon: UserOutlined,
    showInMenu: true,
    component: Members,
  },
  {
    path: '/rule',
    title: 'rule',
    name: 'Quy định',
    icon: TagsOutlined,
    showInMenu: true,
    component: Rule,
  },
  {
    path: '/organization',
    title: 'organization',
    name: 'Tổ chức',
    icon: ApartmentOutlined,
    showInMenu: true,
    component: Organization,
  },
  {
    path: '/*',
    title: 'Not Found',
    name: 'not-found',
    icon: null,
    showInMenu: false,
    component: NotFound,
  },
];

export const routers = [...authRouter, ...appRouters];
