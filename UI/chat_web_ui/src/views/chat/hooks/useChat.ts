import { useChatStore } from '@/store'

export function useChat() {
  const chatStore = useChatStore()

  const getChatByUuidAndIndex = (uuid: number, index: number) => {
    return chatStore.getChatByUuidAndIndex(uuid, index)
  }

  const addChat = (uuid: number, chat: Chat.Chat) => {
    let index = chatStore.addChatByUuid(uuid, chat)
    console.log("useChat addChat: " + index)
    return index
  }

  const updateChat = (uuid: number, index: number, chat: Chat.Chat) => {
    chatStore.updateChatByUuid(uuid, index, chat)
  }

  const updateChat1 = (uuid: number, index:number, msg: string) =>
  {
    console.log("useChat updateChat1: " + index)
    chatStore.updateChatByUuid1(uuid, index, msg)
  }

  const updateChatSome = (uuid: number, index: number, chat: Partial<Chat.Chat>) => {
    chatStore.updateChatSomeByUuid(uuid, index, chat)
  }

  return {
    addChat,
    updateChat,
    updateChat1,
    updateChatSome,
    getChatByUuidAndIndex,
  }
}
