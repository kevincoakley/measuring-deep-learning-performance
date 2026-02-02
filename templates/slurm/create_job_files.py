import argparse, sys
from jinja2 import Environment, FileSystemLoader


def parse_arguments(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--num-job-files",
        dest="num_job_files",
        help="Number of job files to create",
        type=int,
        default=10,
    )

    parser.add_argument(
        "--hpc-cluster",
        dest="hpc_cluster",
        help="Name of the HPC cluster",
        default="idun",
        choices=[
            "idun",
        ],
    )

    parser.add_argument(
        "--gpu",
        dest="gpu",
        help="Type of GPU",
        default="A100",
        choices=[
            "A100",
            "V100",
        ],
        required=True,
    )

    parser.add_argument(
        "--container-short",
        dest="container_short",
        help="Container short name",
        default="ngc2312",
        choices=["ngc2312"],
        required=True,
    )

    parser.add_argument(
        "--ml-framework",
        dest="machine_learning_framework",
        help="Name of Machine Learning framework",
        default="TensorFlow",
        choices=[
            "TensorFlow",
            "PyTorch",
        ],
        required=True,
    )

    parser.add_argument(
        "--model-name",
        dest="model_name",
        help="Name of model to train",
        default="DenseNet121",
        choices=[
            "DenseNet_k12d40",
            "DenseNet_k12d100",
            "DenseNet_k24d100",
            "DenseNet_bc_k12d100",
            "DenseNet_bc_k24d250",
            "DenseNet_bc_k40d190",
            "DenseNet121",
            "DenseNet169",
            "DenseNet201",
            "DenseNet264",
            "ResNet20",
            "ResNet32",
            "ResNet44",
            "ResNet56",
            "ResNet110",
            "ResNet1202",
            "ResNet18",
            "ResNet34",
            "ResNet50",
            "ResNet101",
            "ResNet152",
            "ViTS8",
            "ViTB8",
            "ViTTiny16",
            "ViTS16",
            "ViTB16",
            "ViTL16",
            "ViTH16",
        ],
        required=True,
    )

    parser.add_argument(
        "--dataset-name",
        dest="dataset_name",
        help="Name of dataset to use",
        default="cifar10",
        choices=[
            "cats_vs_dogs",
            "cifar10",
            "cifar10_224",
            "cifar100",
            "cifar100_224",
            "imagenette",
            "oxford_flowers102",
            "oxford_iiit_pet",
            "uc_merced",
        ],
        required=True,
    )

    parser.add_argument(
        "--optimizer",
        dest="optimizer",
        help="Name of optimizer to use",
        default="SGD",
        choices=[
            "SGD",
            "Adam",
            "AdamW",
        ],
        required=True,
    )

    parser.add_argument(
        "--epochs",
        dest="epochs",
        help="Number of epochs",
        type=int,
        default=0,
    )

    parser.add_argument(
        "--batch-size",
        dest="batch_size",
        help="Size of the mini-batches",
        type=int,
        default=128,
    )
    parser.add_argument(
        "--learning-rate",
        dest="learning_rate",
        help="Base learning rate",
        type=float,
        default=0.001,
    )

    parser.add_argument(
        "--lr-scheduler",
        dest="lr_scheduler",
        help="Use the learning rate scheduler",
        action="store_true",
    )

    parser.add_argument(
        "--lr-warmup",
        dest="lr_warmup",
        help="Use the learning rate warmup of 5 epochs",
        action="store_true",
    )

    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])

    # Set container file name
    if args.machine_learning_framework == "PyTorch":
        if args.container_short == "ngc2312":
            container_filename = "pytorch_23.12-py3-1.1.1.sif"
    elif args.machine_learning_framework == "TensorFlow":
        if args.container_short == "ngc2312":
            container_filename = "tensorflow_23.12-tf2-py3-1.0.1.sif"


    if args.lr_scheduler:
        lr_scheduler = "1"
    else:
        lr_scheduler = "0"

    if args.lr_warmup:
        lr_warmup = "1"
    else:
        lr_warmup = "0"


    environment = Environment(loader=FileSystemLoader("./"))
    template = environment.get_template("job.slurm.j2")

    for run in range(args.num_job_files):
        filename = f"job_{run}.slurm"
        content = template.render(
            run_number=run,
            model_name=args.model_name,
            dataset_name=args.dataset_name,
            hpc_cluster=args.hpc_cluster,
            gpu=args.gpu,
            machine_learning_framework=args.machine_learning_framework,
            container_short=args.container_short,
            container_filename=container_filename,
            optimizer=args.optimizer,
            epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.learning_rate,
            lr_scheduler=lr_scheduler,
            lr_warmup=lr_warmup,
        )
        with open(filename, mode="w", encoding="utf-8") as job:
            job.write(content)
            print(f"Writing: {filename}")

    print(
        "%s-%s-%s-%s-%s-%s Done!"
        % (
            args.model_name,
            args.dataset_name.lower(),
            args.hpc_cluster.lower(),
            args.gpu.upper(),
            args.machine_learning_framework,
            args.container_short.lower(),
        )
    )
