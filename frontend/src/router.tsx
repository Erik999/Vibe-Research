import { createHashRouter, Navigate } from "react-router-dom";
import { AlertTriangle } from "lucide-react";
import { Layout } from "@/components/layout/Layout";
import { DailyReview } from "@/pages/DailyReview";
import { Intel } from "@/pages/Intel";
import { Sectors } from "@/pages/Sectors";
import { SectorDetail } from "@/pages/SectorDetail";
import { Portfolio } from "@/pages/Portfolio";
import { StockData } from "@/pages/StockData";
import { Notes } from "@/pages/Notes";
import { Settings } from "@/pages/Settings";

function ErrorPage() {
  return (
    <div className="flex h-screen items-center justify-center">
      <div className="mx-4 max-w-lg rounded-2xl border border-destructive/30 bg-destructive/5 p-8 text-center">
        <AlertTriangle className="mx-auto mb-4 h-8 w-8 text-destructive" />
        <h2 className="mb-2 text-lg font-semibold">页面加载出错</h2>
        <p className="mb-4 text-sm text-muted-foreground">
          可能是数据源暂时不可用或网络波动导致。请尝试刷新页面。
        </p>
        <button
          onClick={() => window.location.reload()}
          className="rounded-lg bg-primary/15 px-4 py-2 text-sm font-medium text-primary hover:bg-primary/25"
        >
          刷新页面
        </button>
      </div>
    </div>
  );
}

export const router = createHashRouter([
  {
    element: <Layout />,
    errorElement: <ErrorPage />,
    children: [
      { path: "/", element: <Navigate to="/daily-review" replace />, errorElement: <ErrorPage /> },
      { path: "/daily-review", element: <DailyReview />, errorElement: <ErrorPage /> },
      { path: "/intel", element: <Intel />, errorElement: <ErrorPage /> },
      { path: "/sectors", element: <Sectors />, errorElement: <ErrorPage /> },
      { path: "/sectors/:key", element: <SectorDetail />, errorElement: <ErrorPage /> },
      { path: "/portfolio", element: <Portfolio />, errorElement: <ErrorPage /> },
      { path: "/stock-data", element: <StockData />, errorElement: <ErrorPage /> },
      { path: "/notes", element: <Notes />, errorElement: <ErrorPage /> },
      { path: "/settings", element: <Settings />, errorElement: <ErrorPage /> },
    ],
  },
]);
