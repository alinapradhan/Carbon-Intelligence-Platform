import { LucideIcon } from 'lucide-react';
export function KpiCard({ title, value, detail, icon: Icon, accent='text-siemens-cyan' }: { title:string; value:string; detail:string; icon:LucideIcon; accent?:string }) {
  return <div className="glass rounded-2xl p-5 hover:-translate-y-1 transition duration-300"><div className="flex items-center justify-between"><span className="text-sm text-slate-400">{title}</span><Icon className={`${accent} h-5 w-5`} /></div><div className="mt-4 text-3xl font-semibold tracking-tight">{value}</div><div className="mt-2 text-xs text-slate-400">{detail}</div></div>;
}
