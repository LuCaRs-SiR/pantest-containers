<script lang="ts">
  import DashboardPanel from '../components/DashboardPanel.svelte';
  import ActivityList from '../components/ActivityList.svelte';
  import MiniChat from '../components/MiniChat.svelte';
  import MiniTerminal from '../components/MiniTerminal.svelte';
  import SystemLogs from '../components/SystemLogs.svelte';
  import { Network, Search, Globe } from '@lucide/svelte';

  const terminalOutput = `Nmap Scan Report for target.com
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
443/tcp open  https

Service detection performed.`;

  const systemLogs = [
    '[00:12:01] nmap-suite container ready',
    '[00:12:03] recon subfinder installed',
    '[00:12:05] ai-gateway connected to ollama',
    '[00:12:07] dashboard initialized'
  ];

  const activities = [
    { time: '2 min ago', message: 'Nmap scan completed on target.com', type: 'success' as const },
    { time: '5 min ago', message: 'Recon found 12 subdomains', type: 'info' as const },
    { time: '12 min ago', message: 'AI flagged critical CVE-2021-44228', type: 'warning' as const }
  ];

  function startScan(tool: string) {
    console.log('Start', tool);
  }
</script>

<h1 class="text-3xl font-black text-cockpit-accent glow-text font-display mb-6">Dashboard</h1>

<div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-6">
  <DashboardPanel
    title="Nmap Scan"
    description="Scan network ports and services"
    icon={Network}
    onstart={() => startScan('nmap')}
  />
  <DashboardPanel
    title="Recon Tools"
    description="Discover subdomains and attack surface"
    icon={Search}
    variant="pink"
    onstart={() => startScan('recon')}
  />
  <DashboardPanel
    title="Web Testing"
    description="Automated web vulnerability checks"
    icon={Globe}
    onstart={() => startScan('web')}
  />
</div>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-6">
  <div class="grid grid-cols-1 gap-5">
    <SystemLogs logs={systemLogs} />
    <MiniTerminal output={terminalOutput} />
  </div>
  <div class="grid grid-cols-1 gap-5">
    <ActivityList {activities} />
    <MiniChat />
  </div>
</div>
