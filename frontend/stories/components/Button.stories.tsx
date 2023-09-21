import { Button } from "@/components/ui/button";
import { Meta, StoryObj } from "@storybook/react";

const meta: Meta<typeof Button> = {
  component: Button,
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Default: Story = {
  render: (args) => <Button {...args}>{args.children}</Button>,
  args: {
    children: "Button",
    variant: "default",
    size: "default",
    asChild: false,
  },
};

export const Destructive: Story = {
  render: (args) => <Button {...args}>{args.children}</Button>,
  args: {
    children: "Button",
    variant: "destructive",
    size: "default",
    asChild: false,
  },
};

export const Outline: Story = {
  render: (args) => <Button {...args}>{args.children}</Button>,
  args: {
    children: "Button",
    variant: "outline",
    size: "default",
    asChild: false,
  },
};

export const Secondary: Story = {
  render: (args) => <Button {...args}>{args.children}</Button>,
  args: {
    children: "Button",
    variant: "secondary",
    size: "default",
    asChild: false,
  },
};

export const Ghost: Story = {
  render: (args) => <Button {...args}>{args.children}</Button>,
  args: {
    children: "Button",
    variant: "ghost",
    size: "default",
    asChild: false,
  },
};

export const Link: Story = {
  render: (args) => <Button {...args}>{args.children}</Button>,
  args: {
    children: "Button",
    variant: "link",
    size: "default",
    asChild: false,
  },
};

export const Null: Story = {
  render: (args) => <Button {...args}>{args.children}</Button>,
  args: {
    children: "Button",
    variant: null,
    size: "default",
    asChild: false,
  },
};
