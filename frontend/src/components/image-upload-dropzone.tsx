import { ImageIcon, X } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import {
  FileUpload,
  FileUploadDropzone,
  FileUploadItem,
  FileUploadItemDelete,
  FileUploadItemMetadata,
  FileUploadItemPreview,
  FileUploadList,
  FileUploadTrigger,
  type FileUploadProps,
} from "@/components/ui/file-upload";
import { useCallback, useState } from "react";
import { uploadImage } from "@/lib/api";

type ImageUploadDropZoneProps = {
  onSetFilename: (filename: string) => void;
};

export function ImageUploadDropZone({
  onSetFilename,
}: ImageUploadDropZoneProps) {
  const [files, setFiles] = useState<File[]>([]);

  const handleFileReject = useCallback((file: File, message: string) => {
    toast.error(message, {
      description: `"${file.name}" was rejected`,
    });
  }, []);

  const handleUpload: NonNullable<FileUploadProps["onUpload"]> = useCallback(
    async (files, { onSuccess, onError }) => {
      try {
        const data = await uploadImage(files[0]);
        onSetFilename(data.filename);
        onSuccess(files[0]);
      } catch (error) {
        onError(
          files[0],
          error instanceof Error ? error : new Error("Upload failed")
        );
      }
    },
    [onSetFilename]
  );

  const handleValueChange = useCallback(
    (newFiles: File[]) => {
      setFiles(newFiles);
      if (newFiles.length === 0) {
        onSetFilename("");
      }
    },
    [onSetFilename]
  );

  return (
    <FileUpload
      accept="image/*"
      maxFiles={1}
      maxSize={8 * 1024 * 1024}
      className="w-full max-w-md"
      value={files}
      onValueChange={handleValueChange}
      onFileReject={handleFileReject}
      onUpload={handleUpload}
      multiple={false}
    >
      <FileUploadDropzone className="border-primary/20 bg-primary/5 hover:bg-primary/10 data-dragging:bg-primary/10">
        <div className="flex flex-col items-center gap-2 text-center">
          <div className="rounded-lg bg-primary/10 p-3">
            <ImageIcon className="size-8 text-primary" />
          </div>
          <div>
            <p className="text-sm font-medium">Upload image</p>
            <p className="text-xs text-muted-foreground">
              PNG, JPG, WEBP, BMP or TIFF up to 8MB
            </p>
          </div>
        </div>
        <FileUploadTrigger asChild>
          <Button size="sm" className="mt-3">
            Select Image
          </Button>
        </FileUploadTrigger>
      </FileUploadDropzone>
      <FileUploadList>
        {files.map((file, index) => (
          <FileUploadItem key={index} value={file}>
            <FileUploadItemPreview />
            <FileUploadItemMetadata />
            <FileUploadItemDelete asChild>
              <Button variant="ghost" size="icon" className="size-7">
                <X className="size-4" />
              </Button>
            </FileUploadItemDelete>
          </FileUploadItem>
        ))}
      </FileUploadList>
    </FileUpload>
  );
}

