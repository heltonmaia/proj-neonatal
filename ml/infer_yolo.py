from ultralytics import YOLO
import cv2

# Função principal para realizar inferência em um vídeo
def inferencia_video(model_path, video_input, output_video):
    # Carregar o modelo YOLOv8
    model = YOLO(model_path)
    
    # Abrir o vídeo de entrada
    cap = cv2.VideoCapture(video_input)
    
    # Verificar se o vídeo foi aberto corretamente
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return
    
    # Configurar as propriedades do vídeo de saída
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Definir o codec e criar o objeto VideoWriter para salvar o vídeo com detecções
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    # Processar cada frame do vídeo
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break  # Sai do loop quando o vídeo acabar
        
        # Realizar inferência no frame
        results = model(frame, imgsz=640, conf=0.5, iou=0.5)
        
        # Extrair o resultado como uma imagem com anotações
        annotated_frame = results[0].plot()
        
        # Salvar o frame processado no vídeo de saída
        out.write(annotated_frame)
        
        # Exibir o frame em tempo real (opcional)
        cv2.imshow("YOLOv8 Inference", annotated_frame)
        
        # Pressione 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Liberar os recursos
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Parâmetros do script
if __name__ == "__main__":
    # Caminho para o modelo treinado (best.pt)
    model_path = "runs/pose/train/weights/best.pt"
    
    # Caminho para o vídeo de entrada
    video_input = "/mnt/hd2/datasets/proj-neonatal/dataset_v1_low/23bancomayararn_ii_adriana/23_ii_adriana_02_pos_low.mp4"
    
    # Caminho para o vídeo de saída com detecções
    output_video = "output_video2.mp4"
    
    # Executar a inferência no vídeo
    inferencia_video(model_path, video_input, output_video)