<script lang="ts">
  import ToolRunner from '../../components/ToolRunner.svelte';
</script>

<ToolRunner
  title="Kali Tools"
  endpoint="/api/kali"
  placeholder="np. nmap --help"
  paramName="command"
/>
