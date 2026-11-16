declare module "lucide-react" {
  import * as React from "react";
  export interface LucideProps extends React.SVGProps<SVGSVGElement> {
    size?: string | number;
    color?: string;
    strokeWidth?: string | number;
    className?: string;
  }
  export type LucideIcon = React.ForwardRefExoticComponent<
    LucideProps & React.RefAttributes<SVGSVGElement>
  >;

  export const LayoutDashboard: LucideIcon;
  export const Bot: LucideIcon;
  export const Workflow: LucideIcon;
  export const CheckSquare: LucideIcon;
  export const ShieldAlert: LucideIcon;
  export const PenTool: LucideIcon;
  export const Image: LucideIcon;
  export const Library: LucideIcon;
  export const Calendar: LucideIcon;
  export const History: LucideIcon;
  export const Database: LucideIcon;
  export const Plug: LucideIcon;
  export const Activity: LucideIcon;
  export const Cpu: LucideIcon;
  export const Settings: LucideIcon;
  export const ChevronLeft: LucideIcon;
  export const ChevronRight: LucideIcon;
  export const Radio: LucideIcon;
  export const Search: LucideIcon;
  export const Bell: LucideIcon;
  export const User: LucideIcon;
  export const CheckCircle: LucideIcon;
  export const CheckCircle2: LucideIcon;
  export const ShieldCheck: LucideIcon;
  export const RefreshCw: LucideIcon;
  export const Table: LucideIcon;
  export const AlertTriangle: LucideIcon;
  export const Play: LucideIcon;
  export const ArrowRight: LucideIcon;
  export const Send: LucideIcon;
  export const Edit3: LucideIcon;
  export const Save: LucideIcon;
  export const Sliders: LucideIcon;
  export const FileText: LucideIcon;
  export const Clock: LucideIcon;
  export const AlertOctagon: LucideIcon;
  export const Sparkles: LucideIcon;
  export const ArrowUpRight: LucideIcon;
  export const TrendingUp: LucideIcon;
  export const Layers: LucideIcon;

  const icons: { [key: string]: LucideIcon };
  export default icons;
}
