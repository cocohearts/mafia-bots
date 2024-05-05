<script>
  import { onMount } from 'svelte';
  import { socket } from '$lib/socketio';

  import Button from '$lib/components/ui/button/button.svelte';
  import Input from '$lib/components/ui/input/input.svelte';

  import { PlusIcon } from 'svelte-feather-icons';

  let chatInputElement;
  const sendChatMessage = () => {
    socket.emit('message', chatInputElement.value);
    chatInputElement.value = '';
  };

  onMount(() => {
    // Socket things
    socket.on('connect', () => {
      console.log(`socket.io connected, id: ${socket.id}`);
      socket.emit('set_username', localStorage.getItem('username'));

      // Welcome message
      messages = [
        ...messages,
        {
          timestamp: new Date(),
          author: 'system',
          content: 'welcome to mafia bots!',
        },
      ];
    });

    socket.on('message', (data) => {
      let raw_timestamp = data.timestamp;
      data.timestamp = new Date(raw_timestamp * 1000);
      messages = [data, ...messages];
    });

    return () => {
      socket.off('connect');
      socket.off('message');
    };
  }, []);

  // Page variables
  let messages = [];
</script>

<div class="flex h-screen flex-col">
  <!-- Navbar -->
  <div class="w-full bg-neutral-100 p-4">
    <div>
      <span class="font-bold">mafia</span>
    </div>
  </div>

  <!-- Main body -->
  <div class="flex flex-grow divide-x overflow-y-hidden">
    <div class="flex w-80 flex-col gap-2 p-2">
      <Button class="flex gap-2" on:click={() => socket.emit('new_game')}>
        <PlusIcon /><span>New game</span></Button
      >
      <Button variant="outline" on:click={() => (messages = [])}
        >Clear chat</Button
      >
    </div>

    <!-- Chat column -->
    <div class="flex w-full flex-col">
      <!-- Chat messages -->
      <table
        class="flex flex-grow border-spacing-2 flex-col-reverse overflow-y-auto"
      >
        {#each messages as message}
          <tr class="px-4 py-1 align-top text-sm">
            <td class="text-muted-foreground whitespace-pre"
              >{message.timestamp.toLocaleTimeString()}</td
            >
            <td class="text-muted-foreground px-2"
              >{message.author.split('-')[0]}</td
            >
            <td>{message.content}</td>
          </tr>
        {/each}
      </table>

      <!-- Chat input -->
      <div class="flex gap-2 p-2">
        <Input
          on:keydown={(e) => e.key === 'Enter' && sendChatMessage()}
          placeholder="Chat with the group..."
          bind:this={chatInputElement}
        />
        <Button on:click={sendChatMessage}>Send</Button>
      </div>
    </div>
  </div>
</div>
