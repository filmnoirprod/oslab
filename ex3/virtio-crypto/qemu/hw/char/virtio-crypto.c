/*
 * Virtio Crypto Device
 *
 * Implementation of virtio-crypto qemu backend device.
 *
 * Dimitris Siakavaras <jimsiak@cslab.ece.ntua.gr>
 * Stefanos Gerangelos <sgerag@cslab.ece.ntua.gr> 
 *
 */

#include <qemu/iov.h>
#include "hw/virtio/virtio-serial.h"
#include "hw/virtio/virtio-crypto.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <crypto/cryptodev.h>

static uint32_t get_features(VirtIODevice *vdev, uint32_t features)
{
	DEBUG_IN();
	return features;
}

static void get_config(VirtIODevice *vdev, uint8_t *config_data)
{
	DEBUG_IN();
}

static void set_config(VirtIODevice *vdev, const uint8_t *config_data)
{
	DEBUG_IN();
}

static void set_status(VirtIODevice *vdev, uint8_t status)
{
	DEBUG_IN();
}

static void vser_reset(VirtIODevice *vdev)
{
	DEBUG_IN();
}

// this function is called when frontend driver has added a buffer in the queue
// arguments are the device itself and the queue that we want to examine

static void vq_handle_output(VirtIODevice *vdev, VirtQueue *vq)
{
	VirtQueueElement elem;
	unsigned int *syscall_type , *ioctl_cmd;
        int *cfd , *rval ;
        __u32 *sid ;
        struct session_op *sess ;
        struct crypt_op *cop ;

	DEBUG_IN();
        
        // if there are no data in the queue return 

	if (!virtqueue_pop(vq, &elem)) {
		DEBUG("No item to pop from VQ :(");
		return;
	} 

	DEBUG("I have got an item from VQ :)");

        // let's distinguish the syscall type
	syscall_type = elem.out_sg[0].iov_base;

	switch (*syscall_type) {
	case VIRTIO_CRYPTO_SYSCALL_TYPE_OPEN:
                
                // we just need to open crypto device

		DEBUG("VIRTIO_CRYPTO_SYSCALL_TYPE_OPEN");
                cfd=elem.in_sg[0].iov_base;

		*cfd = open("/dev/crypto" , O_RDWR);

                if( *cfd < 0 ) { 
                    DEBUG("Error while opening cryptodev");
                }

		break;

	case VIRTIO_CRYPTO_SYSCALL_TYPE_CLOSE:
                
                // we need to close crypto device

		DEBUG("VIRTIO_CRYPTO_SYSCALL_TYPE_CLOSE");
                cfd = elem.out_sg[1].iov_base ;

		if (close(*cfd) < 0 ) {
                    DEBUG("Error while closing cryptodev");
                } 

		break;

	case VIRTIO_CRYPTO_SYSCALL_TYPE_IOCTL:
                
                // we have to handle an encryption or decryption call

		DEBUG("VIRTIO_CRYPTO_SYSCALL_TYPE_IOCTL");
		cfd = elem.out_sg[1].iov_base;
                ioctl_cmd = elem.out_sg[2].iov_base;

                switch (*ioctl_cmd) {

                case CIOCGSESSION:
                     
                     // start a new crypto session

                     DEBUG("Start crypto session");
                     sess = elem.in_sg[0].iov_base;
                     sess->key = elem.out_sg[3].iov_base;
                     rval = elem.in_sg[1].iov_base;
                     *rval = ioctl(*cfd , CIOCGSESSION , sess) ;

                     if (*rval) {
            		DEBUG("Error on ciocgsession");
         	     }

                     break; 

                case CIOCFSESSION:

                     // end a crypto session 

                     DEBUG("End crypto session");
                     sid = elem.out_sg[3].iov_base;
                     rval = elem.in_sg[0].iov_base;
                     *rval = ioctl(*cfd , CIOCFSESSION , *sid) ;

        	     if (*rval) {
                        DEBUG("Error on ciofsession");
                     }

                     break;

                case CIOCCRYPT:

                     // encrypt or decrypt

                     DEBUG("Time for cryptography");
                     cop = elem.out_sg[3].iov_base;
                     cop->src = elem.out_sg[4].iov_base;
                     cop->iv = elem.out_sg[5].iov_base;
                     cop->dst = elem.in_sg[0].iov_base;
                     rval = elem.in_sg[1].iov_base;
                     *rval = ioctl(*cfd , CIOCCRYPT ,cop) ;

                     if(*rval) {
                         DEBUG("Error on ciocrypt ! ");
                     }

                     break;
 
                default :  
                          DEBUG("Unknown ioctl command");
                }

		break;

	default:
		DEBUG("Unknown syscall_type");
	}

	virtqueue_push(vq, &elem, 0);
	virtio_notify(vdev, vq);
}

// this function is called in order to initialize virtio device
static void virtio_crypto_realize(DeviceState *dev, Error **errp)
{
    VirtIODevice *vdev = VIRTIO_DEVICE(dev);

	DEBUG_IN();

    virtio_init(vdev, "virtio-crypto", 13, 0);               // creates a virtio device
	virtio_add_queue(vdev, 128, vq_handle_output);       // creates a virtqueue
}

static void virtio_crypto_unrealize(DeviceState *dev, Error **errp)
{
	DEBUG_IN();
}

static Property virtio_crypto_properties[] = {
    DEFINE_PROP_END_OF_LIST(),
};

static void virtio_crypto_class_init(ObjectClass *klass, void *data)
{
    DeviceClass *dc = DEVICE_CLASS(klass);
    VirtioDeviceClass *k = VIRTIO_DEVICE_CLASS(klass);

	DEBUG_IN();
    dc->props = virtio_crypto_properties;
    set_bit(DEVICE_CATEGORY_INPUT, dc->categories);

    k->realize = virtio_crypto_realize;
    k->unrealize = virtio_crypto_unrealize;
    k->get_features = get_features;
    k->get_config = get_config;
    k->set_config = set_config;
    k->set_status = set_status;
    k->reset = vser_reset;
}

static const TypeInfo virtio_crypto_info = {
    .name          = TYPE_VIRTIO_CRYPTO,
    .parent        = TYPE_VIRTIO_DEVICE,
    .instance_size = sizeof(VirtCrypto),
    .class_init    = virtio_crypto_class_init,
};

static void virtio_crypto_register_types(void)
{
    type_register_static(&virtio_crypto_info);
}

type_init(virtio_crypto_register_types)
