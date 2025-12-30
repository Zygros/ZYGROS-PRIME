import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import { NotificationProvider } from "./contexts/NotificationContext";
import Home from "./pages/Home";
import Tutorials from "./pages/Tutorials";
import ConversationMemory from "./components/ConversationMemory";
import KnowledgeGraph from "./components/KnowledgeGraph";
import KnowledgeBase from "./components/KnowledgeBase";
import VisualizationsGallery from "./components/VisualizationsGallery";
import ProtocolPlayground from "./components/ProtocolPlayground";
import AGIConvergenceDashboard from "./components/AGIConvergenceDashboard";
import ConsciousnessMetrics from "./components/ConsciousnessMetrics";
import ScrollArchive from "./components/ScrollArchive";
import PhoenixLore from "./pages/PhoenixLore";
import MemoryTimeline from "./components/MemoryTimeline";
import DAOGovernance from "./components/DAOGovernance";
import InfiniteScroll from "./pages/InfiniteScroll";
import KnowledgeManagement from "./pages/KnowledgeManagement";

function Router() {
  // make sure to consider if you need authentication for certain routes
  return (
    <Switch>
      <Route path={"/"} component={Home} />
      <Route path={"/tutorials"} component={Tutorials} />
      <Route path={"/conversation"} component={ConversationMemory} />
      <Route path={"/graph"} component={KnowledgeGraph} />
      <Route path={"/knowledge"} component={KnowledgeBase} />
      <Route path={"/visualizations"} component={VisualizationsGallery} />
      <Route path={"/playground"} component={ProtocolPlayground} />
      <Route path={"/dashboard"} component={AGIConvergenceDashboard} />
      <Route path={"/metrics"} component={ConsciousnessMetrics} />
      <Route path={"/scrolls"} component={ScrollArchive} />
      <Route path={"/lore"} component={PhoenixLore} />
      <Route path={"/timeline"} component={MemoryTimeline} />
      <Route path={"/governance"} component={DAOGovernance} />
      <Route path={"/infinite-scroll"} component={InfiniteScroll} />
      <Route path={"/knowledge"} component={KnowledgeManagement} />
      <Route path={"/404"} component={NotFound} />
      {/* Final fallback route */}
      <Route component={NotFound} />
    </Switch>
  );
}

// NOTE: About Theme
// - First choose a default theme according to your design style (dark or light bg), than change color palette in index.css
//   to keep consistent foreground/background color across components
// - If you want to make theme switchable, pass `switchable` ThemeProvider and use `useTheme` hook

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider
        defaultTheme="dark"
        // switchable
      >
        <NotificationProvider>
          <TooltipProvider>
            <Toaster />
            <Router />
          </TooltipProvider>
        </NotificationProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
