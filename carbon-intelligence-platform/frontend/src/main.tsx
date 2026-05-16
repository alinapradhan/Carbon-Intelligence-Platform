import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { Dashboard } from './components/Dashboard';
import { Sidebar } from './components/Sidebar';
ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><div className="flex min-h-screen"><Sidebar/><Dashboard/></div></React.StrictMode>);
