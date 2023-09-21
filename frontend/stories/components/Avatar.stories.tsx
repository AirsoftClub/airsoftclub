import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Meta, StoryObj } from "@storybook/react";

const meta: Meta<typeof Avatar> = {
  component: Avatar,
};

export default meta;
type Story = StoryObj<typeof Avatar>;

export const Default: Story = {
  render: () => (
    <Avatar>
      <AvatarFallback>NK</AvatarFallback>
    </Avatar>
  ),
};
