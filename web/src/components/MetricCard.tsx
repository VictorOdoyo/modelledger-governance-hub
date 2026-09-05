import type { LucideIcon } from 'lucide-react';

interface Props {
  icon: LucideIcon;
  label: string;
  value: string;
  detail: string;
}

export function MetricCard({ icon: Icon, label, value, detail }: Props) {
  return (
    <article className="metric-card">
      <Icon size={18} />
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </article>
  );
}
