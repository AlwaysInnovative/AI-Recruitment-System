declare module 'react-quill' {
  import { Component, ReactNode } from 'react';
  
  interface ReactQuillProps {
    value?: string;
    defaultValue?: string;
    onChange?: (content: string, delta: any, source: string, editor: any) => void;
    onChangeSelection?: (range: any, source: string, editor: any) => void;
    onFocus?: (range: any, source: string, editor: any) => void;
    onBlur?: (previousRange: any, source: string, editor: any) => void;
    onKeyPress?: () => void;
    onKeyDown?: () => void;
    onKeyUp?: () => void;
    placeholder?: string;
    modules?: Record<string, any>;
    formats?: string[];
    theme?: string;
    style?: React.CSSProperties;
    className?: string;
    readOnly?: boolean;
    bounds?: string | HTMLElement;
    scrollingContainer?: string | HTMLElement;
    children?: ReactNode;
  }

  export default class ReactQuill extends Component<ReactQuillProps> {}
  export const Quill: any;
}
