declare module 'react-quill' {
  import { Component } from 'react';
  
  interface ReactQuillProps {
    value?: string;
    defaultValue?: string;
    onChange?: (value: string) => void;
    placeholder?: string;
    modules?: Record<string, unknown>;
    formats?: string[];
    theme?: string;
    style?: React.CSSProperties;
    className?: string;
    readOnly?: boolean;
  }

  export default class ReactQuill extends Component<ReactQuillProps> {}
}
