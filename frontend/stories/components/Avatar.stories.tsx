import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Meta, StoryObj } from "@storybook/react";

const meta: Meta<typeof Avatar> = {
  component: Avatar,
};

export default meta;
type Story = StoryObj<typeof Avatar>;

export const Default: Story = {
  render: (args) => (
    <Avatar {...args}>
      <AvatarImage
        src="https://avatars.githubusercontent.com/u/1024025?v=4"
        alt="avatar"
      />
    </Avatar>
  ),
};

export const WithFallback: Story = {
  render: (args) => (
    <Avatar {...args}>
      <AvatarImage alt="avatar" />
      <AvatarFallback>LT</AvatarFallback>
    </Avatar>
  ),
};
