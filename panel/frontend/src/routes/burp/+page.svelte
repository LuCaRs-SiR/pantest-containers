<script lang="ts">
  import ToolRunner from '../../components/ToolRunner.svelte';
</script>

<ToolRunner
  title="Burp"
  endpoint="/api/burp"
  placeholder="np. burpsuite --help"
  paramName="command"
/>
